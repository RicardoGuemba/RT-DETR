# 🚀 Como Usar o Executável

## ✅ Executável Criado com Sucesso!

**✅ CORRIGIDO PARA macOS 15.6 (Sequoia)**
- Removida dependência do framework Carbon (incompatível com macOS 15.6)
- Bundle .app criado manualmente para compatibilidade moderna
- Info.plist atualizado para macOS 15+

O sistema foi compilado e está pronto para uso. Você tem várias opções para executar:

## 📱 Opção 1: Bundle macOS (.app) - RECOMENDADO

**Localização:** `dist/ObjectDetection_RT-DETR.app`

### Como executar:
1. **No Finder**: Clique duas vezes em `ObjectDetection_RT-DETR.app`
2. **No Terminal**: 
   ```bash
   open dist/ObjectDetection_RT-DETR.app
   ```
3. **Via link simbólico** (se criado):
   ```bash
   open ObjectDetection_RT-DETR.app
   ```

## 📄 Opção 2: Script de Execução

**Arquivo:** `EXECUTAR_SISTEMA.command`

### Como executar:
1. **No Finder**: Clique duas vezes em `EXECUTAR_SISTEMA.command`
2. **No Terminal**:
   ```bash
   ./EXECUTAR_SISTEMA.command
   ```

Este script detecta automaticamente qual executável usar e inicia o sistema.

## 🔧 Opção 3: Executável Direto

**Localização:** `dist/ObjectDetection_RT-DETR/ObjectDetection_RT-DETR`

### Como executar:
```bash
./dist/ObjectDetection_RT-DETR/ObjectDetection_RT-DETR
```

## ⚠️ Primeira Execução

Na primeira execução, o sistema pode:
- Demorar alguns segundos para iniciar (extração de arquivos temporários)
- Baixar modelos do Hugging Face (se necessário)
- Criar estrutura de diretórios em `data/`

Isso é **normal** e acontece apenas na primeira vez.

## 📋 Funcionalidades Disponíveis

Ao executar, você terá acesso a todas as funcionalidades:

✅ **Interface Gráfica Completa**
- Download de datasets do Roboflow
- Treinamento de modelos RT-DETR
- Retomada de treinamento de checkpoints
- Predição em imagens
- Predição em vídeos
- Avaliação de modelos

✅ **Todas as Dependências Incluídas**
- PyTorch (com suporte MPS para Apple Silicon)
- Transformers (Hugging Face)
- OpenCV
- Tkinter
- E todas as outras dependências

## 🔄 Recriar o Executável

Se precisar recriar o executável:

```bash
./create_executable.sh
```

## 📝 Notas Importantes

1. **Tamanho**: O executável é grande (~4GB) porque inclui todas as dependências
2. **Primeira execução**: Pode demorar 5-10 segundos para iniciar
3. **Modelos**: Serão baixados automaticamente na primeira execução
4. **Dados**: Datasets e modelos devem estar em `data/` relativo ao executável

## ❓ Problemas?

### Erro do Carbon Framework (RESOLVIDO ✅)

Se você receber erro sobre Carbon framework:
- **Status**: ✅ CORRIGIDO
- O executável foi reconstruído sem dependência do Carbon
- Compatível com macOS 15.6 (Sequoia) e versões anteriores

### Outros Problemas

Se o executável não funcionar:

1. **Verificar permissões**:
   ```bash
   chmod +x dist/ObjectDetection_RT-DETR.app/Contents/MacOS/ObjectDetection_RT-DETR
   ```

2. **Executar do terminal para ver erros**:
   ```bash
   ./dist/ObjectDetection_RT-DETR.app/Contents/MacOS/ObjectDetection_RT-DETR
   ```

3. **Recriar o executável**:
   ```bash
   ./create_executable.sh
   ```

4. **Verificar compatibilidade macOS**:
   ```bash
   sw_vers  # Deve mostrar macOS 10.15 ou superior
   ```

## 🎉 Pronto!

Agora você pode executar o sistema sem precisar do Cursor ou Python instalado!

