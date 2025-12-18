# Correção: Vídeo de Predição Não Estava Sendo Salvo

## Problema Identificado

O vídeo processado não estava aparecendo no diretório definido por dois motivos:

1. **Modo Preview**: Quando o preview estava ativo, a função `_process_video_with_preview` apenas mostrava o preview em tempo real, mas **não salvava o vídeo**.
2. **Diretório não criado**: O diretório de saída não estava sendo criado antes de processar o vídeo.

## Correções Aplicadas

### 1. Função `_process_video_with_preview` agora salva o vídeo

**Antes:**
- Apenas mostrava preview em tempo real
- Não criava arquivo de vídeo de saída

**Agora:**
- Cria diretório de saída automaticamente
- Inicializa `VideoWriter` para salvar o vídeo processado
- Salva cada frame processado no vídeo de saída
- Fecha o vídeo corretamente ao finalizar
- Mostra mensagem de sucesso com localização do arquivo

### 2. Garantia de criação do diretório de saída

**Antes:**
```python
"--out_path", str(Path(self.inference_output_var.get()) / f"annotated_{Path(input_path).name}"),
```

**Agora:**
```python
# Criar diretório de saída se não existir
output_dir = Path(self.inference_output_var.get())
output_dir.mkdir(parents=True, exist_ok=True)

out_video_path = output_dir / f"annotated_{Path(input_path).name}"
"--out_path", str(out_video_path),
```

### 3. Suporte a preview com salvamento

Quando o preview está ativo, o vídeo agora é:
- Exibido em tempo real na janela de preview
- **E também salvo** no diretório de saída especificado

## Como Funciona Agora

### Modo Normal (sem preview):
1. Processa vídeo usando `src/infer_video.py`
2. Salva vídeo em: `{diretório_saída}/annotated_{nome_video}`
3. Cria CSV e JSON com resultados

### Modo Preview:
1. Processa vídeo diretamente na interface
2. Mostra preview em tempo real
3. **Salva vídeo** em: `{diretório_saída}/annotated_{nome_video}`
4. Mostra mensagem de sucesso ao finalizar

## Arquivos Modificados

- `interface_tkinter.py`:
  - Função `start_inference()`: Cria diretório antes de processar
  - Função `_process_video_with_preview()`: Adiciona salvamento do vídeo

## Teste

Para testar:

1. Abra a interface: `python app.py`
2. Vá para aba "🔮 Predição"
3. Selecione um vídeo
4. Defina diretório de saída (ex: `outputs/inference`)
5. Marque "Exibir preview em tempo real" (opcional)
6. Clique em "Executar Predição"
7. O vídeo será salvo em: `{diretório_saída}/annotated_{nome_video}.mp4`

## Verificação

O vídeo processado deve aparecer no diretório especificado com:
- Nome: `annotated_{nome_original}.mp4`
- CSV: `annotated_{nome_original}_detections.csv`
- JSON: `annotated_{nome_original}_predictions.json`

