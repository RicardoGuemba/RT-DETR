"""
Utilitários para carregar modelo + processor (Transformers) de forma robusta.

Objetivo:
- Centralizar a lógica de carregamento para treino/avaliação/inferência
- Suporte EXCLUSIVO para RT-DETR v1 (SEM suporte para RT-DETRv2)
- Usa Auto* (o processor correto vem do checkpoint)
- Evitar "pip install" em runtime (melhores práticas)

IMPORTANTE: Este sistema requer RT-DETR v1 exclusivamente.
Modelos RT-DETRv2 serão rejeitados automaticamente.

Modelos suportados (RT-DETR v1 apenas):
- PekingU/rtdetr_r50vd (padrão)
- PekingU/rtdetr_r101vd
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple, Dict, Any


@dataclass(frozen=True)
class LoadedHFObjectDetection:
    processor: Any
    model: Any
    resolved_model_name_or_path: str


def _size_dict(img_size: Optional[int]) -> Optional[Dict[str, int]]:
    if not img_size:
        return None
    # RT-DETR/DETR tipicamente aceita {height,width}. AutoImageProcessor lida com isso quando suportado.
    return {"height": int(img_size), "width": int(img_size)}


def load_processor(model_name_or_path: str, img_size: Optional[int] = None):
    """
    Carrega o processor do checkpoint.
    - Usa AutoImageProcessor como caminho principal
    - Faz fallback para DetrImageProcessor apenas se necessário
    """
    from transformers import AutoImageProcessor, DetrImageProcessor

    size = _size_dict(img_size)
    try:
        if size:
            return AutoImageProcessor.from_pretrained(model_name_or_path, size=size)
        return AutoImageProcessor.from_pretrained(model_name_or_path)
    except Exception:
        # Fallback (evita quebrar em ambientes antigos/ckpts sem config completa)
        if size:
            return DetrImageProcessor.from_pretrained(model_name_or_path, size=size)
        return DetrImageProcessor.from_pretrained(model_name_or_path)


def _check_rtdetr_support():
    """
    Verifica se o Transformers suporta RT-DETR.
    Retorna (bool, str) indicando suporte e mensagem de erro se não suportado.
    """
    try:
        from transformers import AutoConfig
        from packaging import version
        import transformers
        
        # Verificar versão mínima para RT-DETR v1
        transformers_version = version.parse(transformers.__version__)
        required_version = version.parse("4.35.0")
        
        if transformers_version < required_version:
            return False, (
                f"Transformers versão {transformers.__version__} não suporta RT-DETR.\n"
                f"Versão mínima requerida: 4.35.0\n"
                f"Atualize com: pip install --upgrade 'transformers>=4.35.0'"
            )
        
        # Tentar carregar config do RT-DETR para verificar suporte
        try:
            config = AutoConfig.from_pretrained("PekingU/rtdetr_r50vd", _fast_init=False)
            if not hasattr(config, 'model_type') or 'rt_detr' not in config.model_type.lower():
                return False, (
                    "RT-DETR não está disponível no Transformers instalado.\n"
                    "Atualize com: pip install --upgrade 'transformers>=4.35.0'"
                )
        except Exception as e:
            return False, (
                f"Não foi possível verificar suporte ao RT-DETR.\n"
                f"Erro: {e}\n"
                f"Atualize com: pip install --upgrade 'transformers>=4.35.0'"
            )
        
        return True, ""
    except ImportError:
        return False, (
            "Transformers não está instalado.\n"
            "Instale com: pip install 'transformers>=4.35.0'"
        )


def load_model_for_object_detection(
    model_name_or_path: str,
    *,
    num_labels: Optional[int] = None,
    id2label: Optional[Dict[int, str]] = None,
    label2id: Optional[Dict[str, int]] = None,
    ignore_mismatched_sizes: bool = True,
    allow_v2_for_local: bool = True,
):
    """
    Carrega um modelo RT-DETR via AutoModelForObjectDetection.
    
    IMPORTANTE: Para novos treinamentos, este sistema requer RT-DETR v1 exclusivamente.
    Para modelos já treinados salvos localmente, RT-DETRv2 pode ser carregado com aviso.
    
    Args:
        model_name_or_path: Nome do modelo RT-DETR v1 (ex: PekingU/rtdetr_r50vd) ou caminho local
        num_labels: Número de classes
        id2label: Mapeamento id -> label
        label2id: Mapeamento label -> id
        ignore_mismatched_sizes: Ignorar tamanhos incompatíveis
        allow_v2_for_local: Se True, permite RT-DETRv2 para modelos locais (já treinados)
    """
    from transformers import AutoModelForObjectDetection, AutoConfig
    from pathlib import Path
    
    # Verificar se é um caminho local ou nome do HuggingFace
    # Um caminho local pode ser absoluto ou relativo, e geralmente contém "/" mas não começa com http/https
    model_path_obj = Path(model_name_or_path)
    is_local_path = (
        model_path_obj.exists() or 
        (model_path_obj.is_absolute() and model_path_obj.parent.exists()) or
        ("/" in model_name_or_path and not model_name_or_path.startswith(("http://", "https://")) and 
         not "/" in model_name_or_path.split("/")[0] or len(model_name_or_path.split("/")) > 1)
    )
    
    # Para modelos locais, ser mais permissivo - permitir qualquer RT-DETR
    # Validar que NÃO é RT-DETRv2 apenas se for um nome de modelo do HuggingFace
    if not is_local_path:
        model_name_lower = model_name_or_path.lower()
        if "rtdetr_v2" in model_name_lower or "rt-detr-v2" in model_name_lower or "rtdetrv2" in model_name_lower:
            raise ValueError(
                f"❌ ERRO: Este sistema requer RT-DETR v1 exclusivamente para novos treinamentos.\n"
                f"Modelo fornecido: {model_name_or_path}\n"
                f"Este modelo é RT-DETRv2 e não é suportado por este sistema.\n\n"
                f"Modelos válidos (RT-DETR v1):\n"
                f"- PekingU/rtdetr_r50vd (padrão)\n"
                f"- PekingU/rtdetr_r101vd\n\n"
                f"Para usar RT-DETRv2, utilize outro sistema."
            )
    
    # Verificar suporte ao RT-DETR
    is_supported, error_msg = _check_rtdetr_support()
    if not is_supported:
        raise RuntimeError(
            f"❌ ERRO: RT-DETR não está disponível.\n\n"
            f"{error_msg}\n\n"
            f"SOLUÇÃO:\n"
            f"1. Atualize o Transformers: pip install --upgrade 'transformers>=4.35.0'\n"
            f"2. Instale todas as dependências: pip install -r requirements.txt"
        )

    # Tentar carregar a configuração para validar o tipo do modelo
    try:
        config = AutoConfig.from_pretrained(model_name_or_path)
        model_type = getattr(config, "model_type", "").lower()
        
        # Para modelos locais, ser mais permissivo - aceitar qualquer RT-DETR (v1 ou v2)
        # Apenas validar estritamente para modelos do HuggingFace
        if "rt_detr_v2" in model_type or "rtdetr_v2" in model_type:
            if is_local_path and allow_v2_for_local:
                print(f"⚠️  AVISO: O modelo '{model_name_or_path}' pode ser RT-DETRv2.")
                print(f"   Este modelo será carregado para compatibilidade com modelos já treinados.")
                print(f"   Para novos treinamentos, use RT-DETR v1 (PekingU/rtdetr_r50vd).")
            else:
                raise ValueError(
                    f"❌ ERRO: O modelo '{model_name_or_path}' é RT-DETRv2.\n"
                    f"Este sistema requer RT-DETR v1 exclusivamente.\n\n"
                    f"Modelos válidos (RT-DETR v1):\n"
                    f"- PekingU/rtdetr_r50vd\n"
                    f"- PekingU/rtdetr_r101vd\n\n"
                    f"Para usar RT-DETRv2, utilize outro sistema."
                )
        elif is_local_path and ("rt_detr" in model_type or "rtdetr" in model_type):
            # Modelo local RT-DETR (v1) - permitir sem restrições
            print(f"   ✅ Modelo RT-DETR detectado (caminho local)")
        
        # Validar que é RT-DETR (v1 ou v2 se permitido)
        if "rt_detr" not in model_type and "rtdetr" not in model_type:
            raise ValueError(
                f"❌ ERRO: O modelo '{model_name_or_path}' não é RT-DETR.\n"
                f"Tipo detectado: '{model_type}'\n"
                f"Este sistema requer RT-DETR.\n\n"
                f"Modelos válidos:\n"
                f"- PekingU/rtdetr_r50vd (RT-DETR v1)\n"
                f"- PekingU/rtdetr_r101vd (RT-DETR v1)"
            )
    except ValueError:
        # Re-raise ValueError (nossas validações)
        raise
    except Exception as e:
        # Se não conseguir carregar config, continuar (pode ser problema de conexão)
        print(f"⚠️  Aviso: Não foi possível validar o tipo do modelo via config: {e}")
        print(f"   Continuando com carregamento do modelo...")

    kwargs: Dict[str, Any] = {"ignore_mismatched_sizes": ignore_mismatched_sizes}
    if num_labels is not None:
        kwargs["num_labels"] = int(num_labels)
    if id2label is not None:
        kwargs["id2label"] = id2label
    if label2id is not None:
        kwargs["label2id"] = label2id

    try:
        model = AutoModelForObjectDetection.from_pretrained(model_name_or_path, **kwargs)
        
        # Validação final: verificar que o modelo carregado é RT-DETR
        config = model.config
        model_type = getattr(config, "model_type", "").lower()
        
        if "rt_detr_v2" in model_type or "rtdetr_v2" in model_type:
            if is_local_path and allow_v2_for_local:
                print(f"   ✅ Modelo RT-DETR carregado (modo compatibilidade para modelo já treinado)")
            else:
                raise RuntimeError(
                    f"❌ ERRO: O modelo carregado é RT-DETRv2.\n"
                    f"Tipo do modelo: '{model_type}'\n"
                    f"Este sistema requer RT-DETR v1 exclusivamente.\n\n"
                    f"Modelos válidos:\n"
                    f"- PekingU/rtdetr_r50vd\n"
                    f"- PekingU/rtdetr_r101vd\n\n"
                    f"Para usar RT-DETRv2, utilize outro sistema."
                )
        elif "rt_detr" in model_type or "rtdetr" in model_type:
            if is_local_path:
                print(f"   ✅ Modelo RT-DETR carregado!")
            else:
                print(f"   ✅ Modelo RT-DETR v1 carregado!")
        
        if "rt_detr" not in model_type and "rtdetr" not in model_type:
            raise RuntimeError(
                f"❌ ERRO: O modelo carregado não é RT-DETR.\n"
                f"Tipo do modelo: '{model_type}'\n"
                f"Este sistema requer RT-DETR."
            )
        
        return model
    except (ValueError, RuntimeError) as e:
        # Re-raise nossas validações
        raise
    except (ValueError, KeyError) as e:
        raise RuntimeError(
            f"❌ ERRO: Não foi possível carregar RT-DETR.\n\n"
            f"Modelo: {model_name_or_path}\n"
            f"Erro: {e}\n\n"
            f"SOLUÇÃO:\n"
            f"1. Verifique o nome do modelo (ex: PekingU/rtdetr_r50vd)\n"
            f"2. Atualize o Transformers: pip install --upgrade 'transformers>=4.35.0'\n"
            f"3. Verifique sua conexão com internet (download do modelo)\n"
            f"4. Certifique-se de que o modelo é RT-DETR v1 (não v2)"
        ) from e


def load_model_and_processor(
    model_name_or_path: str,
    *,
    img_size: Optional[int] = None,
    num_labels: Optional[int] = None,
    id2label: Optional[Dict[int, str]] = None,
    label2id: Optional[Dict[str, int]] = None,
    ignore_mismatched_sizes: bool = True,
) -> LoadedHFObjectDetection:
    """
    Helper único: processor + model.
    
    Carrega modelo RT-DETR v1 e seu processor correspondente.
    
    IMPORTANTE: Este sistema requer RT-DETR v1 exclusivamente.
    Modelos RT-DETRv2 serão rejeitados automaticamente.
    """
    processor = load_processor(model_name_or_path, img_size=img_size)
    model = load_model_for_object_detection(
        model_name_or_path,
        num_labels=num_labels,
        id2label=id2label,
        label2id=label2id,
        ignore_mismatched_sizes=ignore_mismatched_sizes,
    )
    
    return LoadedHFObjectDetection(
        processor=processor,
        model=model,
        resolved_model_name_or_path=model_name_or_path,
    )


