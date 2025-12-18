#!/usr/bin/env python3
"""
Script para fazer inferência com modelo DETR/RT-DETR treinado - ObjectDetection_RT-DETR.
"""

import os
import json
import argparse
import warnings

# Configurar ambiente ANTES de importar transformers
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")

from pathlib import Path
import torch
from PIL import Image, ImageDraw, ImageFont
from transformers import AutoImageProcessor, AutoModelForObjectDetection, DetrImageProcessor
from tqdm import tqdm
import numpy as np
import uuid
import csv
from datetime import datetime

from coco_utils import load_coco_json

# Suprimir warnings específicos
warnings.filterwarnings("ignore", category=UserWarning, module="torch.nn.modules.module")
warnings.filterwarnings("ignore", message=".*copying from a non-meta parameter.*")
warnings.filterwarnings("ignore", message=".*Using a slow image processor.*")
warnings.filterwarnings("ignore", message=".*use_fast.*")
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", message=".*Some weights.*were not used.*")
warnings.filterwarnings("ignore", message=".*Some weights.*were not initialized.*")


def get_device():
    """Retorna device disponível (MPS ou CPU)."""
    if torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


def draw_bbox(image, bbox, label, score, color=(255, 0, 0), width=2, control_id=None, show_control_id=False):
    """
    Desenha bounding box na imagem.
    
    Args:
        image: PIL Image
        bbox: [x1, y1, x2, y2]
        label: String com label
        score: Score da predição
        color: Cor RGB
        width: Largura da linha
        control_id: ID único de controle (opcional)
        show_control_id: Se True, exibe o control_id no texto
    """
    draw = ImageDraw.Draw(image)
    x1, y1, x2, y2 = bbox
    
    # Desenhar retângulo
    draw.rectangle([x1, y1, x2, y2], outline=color, width=width)
    
    # Texto com label e score
    text = f"{label} {score:.2f}"
    if show_control_id and control_id is not None:
        # Usar apenas os primeiros 8 caracteres do UUID para legibilidade
        short_id = str(control_id)[:8]
        text = f"{label} {score:.2f} [{short_id}]"
    
    # Tentar carregar fonte, usar padrão se falhar
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
    except:
        font = ImageFont.load_default()
    
    # Calcular tamanho do texto
    bbox_text = draw.textbbox((0, 0), text, font=font)
    text_width = bbox_text[2] - bbox_text[0]
    text_height = bbox_text[3] - bbox_text[1]
    
    # Desenhar fundo do texto
    draw.rectangle(
        [x1, y1 - text_height - 4, x1 + text_width + 4, y1],
        fill=color
    )
    
    # Desenhar texto
    draw.text((x1 + 2, y1 - text_height - 2), text, fill=(255, 255, 255), font=font)


def infer_images(
    model_dir: Path,
    input_dir: Path,
    out_dir: Path,
    score_threshold: float = 0.8,
    iou_threshold: float = 0.5,
    dataset_dir: Path = None,
    input_file: Path = None,
    show_control_id: bool = False
):
    """
    Faz inferência em uma pasta de imagens, arquivo único (imagem ou vídeo).
    
    Args:
        model_dir: Diretório contendo o modelo
        input_dir: Diretório com imagens de entrada (se input_file não fornecido)
        out_dir: Diretório de saída
        score_threshold: Threshold mínimo de score
        iou_threshold: IOU threshold (nota: RT-DETR já aplica NMS internamente)
        dataset_dir: Diretório do dataset (para obter nomes de categorias)
        input_file: Arquivo único (imagem ou vídeo) - se fornecido, ignora input_dir
        show_control_id: Se True, exibe o control_id nas imagens anotadas
    """
    device = get_device()
    print(f"🔧 Device: {device}")
    
    # Carregar modelo (suprimir warnings)
    print(f"📥 Carregando modelo de {model_dir}...")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        model = AutoModelForObjectDetection.from_pretrained(str(model_dir))
    model.to(device)
    model.eval()
    
    # Carregar processor com fallback (suprimir warnings)
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            processor = AutoImageProcessor.from_pretrained(str(model_dir))
    except (ValueError, OSError):
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                processor = DetrImageProcessor.from_pretrained(str(model_dir))
        except Exception:
            # Criar processador genérico
            processor = DetrImageProcessor(
                format="coco_detection",
                size={"shortest_edge": 640, "longest_edge": 640},
                do_resize=True,
                do_normalize=True,
                do_rescale=True,
                image_mean=[0.485, 0.456, 0.406],
                image_std=[0.229, 0.224, 0.225]
            )
    
    # Carregar nomes de categorias se disponível
    category_names = {}
    if dataset_dir:
        try:
            # Tentar carregar de qualquer split disponível
            for split in ["train", "valid", "test"]:
                json_path = dataset_dir / f"{split}/_annotations.coco.json"
                if json_path.exists():
                    coco_data = load_coco_json(json_path)
                    category_names = {
                        cat["id"]: cat["name"]
                        for cat in coco_data["categories"]
                    }
                    break
        except Exception as e:
            print(f"⚠️  Não foi possível carregar nomes de categorias: {e}")
    
    # Verificar se é arquivo único (vídeo ou imagem)
    video_extensions = {".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv"}
    
    if input_file and input_file.exists():
        # Processar arquivo único
        if input_file.suffix.lower() in video_extensions:
            # É um vídeo - usar módulo de vídeo
            print(f"📹 Detectado vídeo: {input_file}")
            try:
                import sys
                from pathlib import Path as PathLib
                sys.path.insert(0, str(PathLib(__file__).parent))
                from infer_video import infer_video
                out_dir.mkdir(parents=True, exist_ok=True)
                out_video_path = out_dir / f"annotated_{input_file.name}"
                infer_video(
                    model_dir=model_dir,
                    video_path=input_file,
                    out_path=out_video_path,
                    score_threshold=score_threshold,
                    dataset_dir=dataset_dir,
                    show_control_id=show_control_id
                )
                return
            except ImportError as e:
                print(f"❌ Erro ao importar módulo infer_video: {e}")
                print("   Certifique-se de que opencv-python está instalado: pip install opencv-python")
                return
            except Exception as e:
                print(f"❌ Erro ao processar vídeo: {e}")
                import traceback
                traceback.print_exc()
                return
        else:
            # É uma imagem única
            print(f"🖼️  Processando imagem única: {input_file}")
            image_files = [input_file]
            input_dir = input_file.parent
            # Garantir que out_dir existe para arquivo único
            out_dir.mkdir(parents=True, exist_ok=True)
    else:
        # Processar diretório de imagens
        out_dir.mkdir(parents=True, exist_ok=True)
        
        # Encontrar imagens
        image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".tiff"}
        image_files = [
            f for f in input_dir.iterdir()
            if f.suffix.lower() in image_extensions
        ]
        
        if len(image_files) == 0:
            print(f"❌ Nenhuma imagem encontrada em {input_dir}")
            return
    
    # Garantir que out_dir existe antes de criar CSV
    out_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📊 Processando {len(image_files)} imagens...")
    
    # Resultados
    all_results = []
    
    # Arquivo CSV para salvar detecções por imagem
    csv_path = out_dir / "detections.csv"
    csv_file = open(csv_path, 'w', newline='', encoding='utf-8')
    csv_writer = csv.writer(csv_file)
    
    # Cabeçalhos do CSV
    csv_headers = [
        "image_name",
        "control_id",
        "category_id",
        "category_name",
        "score",
        "bbox_x1",
        "bbox_y1",
        "bbox_x2",
        "bbox_y2",
        "bbox_width",
        "bbox_height",
        "bbox_center_x",
        "bbox_center_y",
        "image_width",
        "image_height",
        "detection_timestamp"
    ]
    csv_writer.writerow(csv_headers)
    
    # Buffer para escrita CSV em lote (otimização)
    csv_buffer = []
    csv_buffer_size = 100  # Escrever a cada 100 detecções
    control_id_counter = 0  # Contador sequencial (mais rápido que UUID)
    
    print(f"   CSV será salvo em: {csv_path}")
    print(f"   ⚡ Otimização: Buffer de {csv_buffer_size} detecções para escrita em lote\n")
    
    with torch.no_grad():
        for img_path in tqdm(image_files, desc="Processando"):
            # Carregar imagem
            image = Image.open(img_path).convert("RGB")
            original_size = image.size
            
            # Processar
            inputs = processor(images=image, return_tensors="pt")
            inputs = {k: v.to(device) for k, v in inputs.items()}
            
            # Fazer predição
            outputs = model(**inputs)
            
            # Processar outputs
            target_sizes = torch.tensor([image.size[::-1]]).to(device)
            results = processor.post_process_object_detection(
                outputs,
                target_sizes=target_sizes,
                threshold=score_threshold
            )[0]
            
            # Nota: IOU threshold é usado internamente pelo RT-DETR durante o treinamento
            # O post_process_object_detection já aplica NMS com IOU padrão
            # O parâmetro iou_threshold é mantido para compatibilidade futura
            
            # Criar cópia da imagem para desenhar
            annotated_image = image.copy()
            img_width, img_height = original_size
            
            # Timestamp único por imagem (otimização)
            image_timestamp = datetime.now().isoformat()
            
            # Desenhar bboxes
            for box, score, label in zip(
                results["boxes"].cpu().numpy(),
                results["scores"].cpu().numpy(),
                results["labels"].cpu().numpy()
            ):
                x1, y1, x2, y2 = box.tolist()
                
                # Gerar ID único de controle (contador sequencial - mais rápido que UUID)
                control_id_counter += 1
                control_id = f"det_{control_id_counter:08d}"
                
                # Obter nome da categoria
                label_name = category_names.get(int(label), f"Class_{int(label)}")
                
                # Calcular informações adicionais do bbox (manter em float para performance)
                bbox_width = x2 - x1
                bbox_height = y2 - y1
                bbox_center_x = (x1 + x2) / 2
                bbox_center_y = (y1 + y2) / 2
                
                # Desenhar
                draw_bbox(
                    annotated_image,
                    [x1, y1, x2, y2],
                    label_name,
                    float(score),
                    control_id=control_id,
                    show_control_id=show_control_id
                )
                
                # Adicionar ao resultado
                all_results.append({
                    "image": img_path.name,
                    "bbox": [float(x1), float(y1), float(x2), float(y2)],
                    "category_id": int(label),
                    "category_name": label_name,
                    "score": float(score),
                    "control_id": control_id
                })
                
                # Adicionar ao buffer CSV (otimização: escrita em lote)
                csv_buffer.append([
                    img_path.name,
                    control_id,
                    int(label),
                    label_name,
                    f"{float(score):.6f}",
                    f"{float(x1):.2f}",
                    f"{float(y1):.2f}",
                    f"{float(x2):.2f}",
                    f"{float(y2):.2f}",
                    f"{bbox_width:.2f}",
                    f"{bbox_height:.2f}",
                    f"{bbox_center_x:.2f}",
                    f"{bbox_center_y:.2f}",
                    img_width,
                    img_height,
                    image_timestamp
                ])
                
                # Escrever buffer quando atingir tamanho limite
                if len(csv_buffer) >= csv_buffer_size:
                    csv_writer.writerows(csv_buffer)
                    csv_buffer.clear()
            
            # Salvar imagem anotada
            out_img_path = out_dir / f"annotated_{img_path.name}"
            annotated_image.save(out_img_path)
    
    # Escrever buffer restante antes de fechar
    if csv_buffer:
        csv_writer.writerows(csv_buffer)
        csv_buffer.clear()
    
    # Fechar arquivo CSV
    csv_file.close()
    
    # Salvar resultados JSON
    results_path = out_dir / "predictions.json"
    with open(results_path, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\n✅ Inferência concluída!")
    print(f"   Imagens salvas em: {out_dir}")
    print(f"   Resultados JSON: {results_path}")
    print(f"   Resultados CSV: {csv_path}")
    print(f"   Total de detecções: {len(all_results)}")


def main():
    parser = argparse.ArgumentParser(description="Fazer inferência com modelo RT-DETR")
    parser.add_argument(
        "--model_dir",
        type=str,
        required=True,
        help="Diretório contendo o modelo"
    )
    parser.add_argument(
        "--input_dir",
        type=str,
        default=None,
        help="Diretório com imagens de entrada (opcional se input_file fornecido)"
    )
    parser.add_argument(
        "--input_file",
        type=str,
        default=None,
        help="Arquivo único (imagem ou vídeo) para processar"
    )
    parser.add_argument(
        "--out_dir",
        type=str,
        required=True,
        help="Diretório de saída"
    )
    parser.add_argument(
        "--score_threshold",
        type=float,
        default=0.8,
        help="Threshold mínimo de score"
    )
    parser.add_argument(
        "--iou_threshold",
        type=float,
        default=0.5,
        help="IOU threshold (nota: RT-DETR já aplica NMS internamente)"
    )
    parser.add_argument(
        "--dataset_dir",
        type=str,
        default=None,
        help="Diretório do dataset (para obter nomes de categorias)"
    )
    parser.add_argument(
        "--show_control_id",
        action="store_true",
        help="Exibir control_id nas imagens anotadas"
    )
    
    args = parser.parse_args()
    
    input_dir_path = Path(args.input_dir) if args.input_dir else None
    input_file_path = Path(args.input_file) if args.input_file else None
    
    if not input_dir_path and not input_file_path:
        parser.error("Forneça --input_dir ou --input_file")
    
    infer_images(
        model_dir=Path(args.model_dir),
        input_dir=input_dir_path or Path("."),
        out_dir=Path(args.out_dir),
        score_threshold=args.score_threshold,
        iou_threshold=args.iou_threshold,
        dataset_dir=Path(args.dataset_dir) if args.dataset_dir else None,
        input_file=input_file_path,
        show_control_id=args.show_control_id
    )


if __name__ == "__main__":
    main()

