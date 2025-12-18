# Changelog - Reorganização e Melhorias

## Data: 2024

### 🎯 Mudanças Principais

#### 1. ✅ Reorganização da Estrutura do Projeto
- Criada estrutura de diretórios organizada seguindo estado da arte:
  - `data/downloads/` - Para downloads de datasets
  - `data/videos/` - Para vídeos de processamento
  - `outputs/models/` - Para modelos treinados
  - `outputs/inference/` - Para resultados de inferência
  - `outputs/logs/` - Para logs de treinamento
  - `docs/` - Documentação adicional movida para pasta dedicada

#### 2. ✅ Threshold Padrão Ajustado para 0.8
- **Antes**: Threshold padrão era 0.3
- **Agora**: Threshold padrão é **0.8** em todos os arquivos:
  - `src/infer_images.py`
  - `src/infer_video.py`
  - `interface_tkinter.py`
  - `interface.py`
- **Benefício**: Melhor precisão nas detecções, reduzindo falsos positivos

#### 3. ✅ Correção da Tela de Predição (Problema Horizontal)
- Ajustada janela de preview em tempo real:
  - Tamanho padrão aumentado: `1400x800` (antes: `1000x700`)
  - Largura máxima de preview aumentada: `1280px` (antes: `640px`)
  - Melhor visualização horizontal sem necessidade de ajuste manual

#### 4. ✅ Hiperparâmetros Avançados de Treinamento
Adicionados novos hiperparâmetros para otimização:

**Parâmetros de Otimização:**
- `weight_decay` (padrão: 0.0001) - Regularização L2
- `warmup_steps` (padrão: 500) - Steps de aquecimento
- `warmup_ratio` (opcional) - Ratio de warmup alternativo
- `lr_scheduler_type` (padrão: "cosine") - Tipo de scheduler:
  - linear, cosine, cosine_with_restarts, polynomial, constant, constant_with_warmup

**Parâmetros do Otimizador Adam:**
- `adam_beta1` (padrão: 0.9)
- `adam_beta2` (padrão: 0.999)
- `adam_epsilon` (padrão: 1e-8)
- `max_grad_norm` (padrão: 1.0) - Gradient clipping

**Aceleração:**
- `fp16` (opcional) - Treinamento em precisão mista (não suportado em MPS)

**Interface:**
- Todos os novos hiperparâmetros disponíveis na interface Tkinter
- Painel de parâmetros com scroll para melhor organização
- Seção "Parâmetros Avançados de Otimização" adicionada

#### 5. ✅ Limpeza e Organização
- Arquivos de documentação movidos para `docs/`
- `.gitignore` atualizado para incluir novos diretórios
- Script de teste `test_setup.py` criado para validar ambiente

### 📝 Arquivos Modificados

1. **src/train_rtdetr.py**
   - Adicionados novos parâmetros na função `train()`
   - Suporte a warmup_ratio alternativo
   - Detecção automática de suporte FP16

2. **interface_tkinter.py**
   - Threshold padrão alterado para 0.8
   - Tela de preview ajustada para melhor visualização horizontal
   - Adicionados campos para novos hiperparâmetros
   - Painel de parâmetros com scroll

3. **src/infer_images.py**
   - Threshold padrão alterado para 0.8

4. **src/infer_video.py**
   - Threshold padrão alterado para 0.8

5. **interface.py**
   - Threshold padrão alterado para 0.8

6. **README.md**
   - Documentação atualizada com nova estrutura
   - Informações sobre novos hiperparâmetros

### 🧪 Testes

Execute `python test_setup.py` para verificar:
- ✅ Imports das dependências
- ✅ Estrutura de diretórios
- ✅ Arquivos principais
- ✅ Thresholds padrão configurados

### 🚀 Como Usar

1. **Treinamento com Hiperparâmetros Avançados:**
   ```bash
   python src/train_rtdetr.py \
     --dataset_dir dataset \
     --out_dir runs_rtdetr \
     --epochs 50 \
     --batch_size 1 \
     --learning_rate 1e-5 \
     --weight_decay 0.0001 \
     --warmup_steps 500 \
     --lr_scheduler_type cosine \
     --adam_beta1 0.9 \
     --adam_beta2 0.999 \
     --max_grad_norm 1.0
   ```

2. **Inferência com Threshold 0.8:**
   ```bash
   python src/infer_images.py \
     --model_dir runs_rtdetr/model_best \
     --input_dir dataset/test \
     --out_dir outputs/inference \
     --score_threshold 0.8
   ```

3. **Interface Gráfica:**
   ```bash
   python app.py
   ```
   - Todos os novos hiperparâmetros disponíveis na aba "Treinamento"
   - Threshold padrão já configurado em 0.8 na aba "Predição"

### ⚠️ Notas Importantes

- **FP16**: Não funciona em MPS (Apple Silicon). O sistema detecta automaticamente e usa FP32.
- **Threshold 0.8**: Pode reduzir o número de detecções, mas aumenta a precisão. Ajuste conforme necessário.
- **Estrutura de Diretórios**: Os diretórios antigos (`runs_rtdetr/`) ainda são suportados para compatibilidade.

