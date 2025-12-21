# 🔧 Correção de Compatibilidade macOS 15.6

## ❌ Problema Identificado

Ao executar o app no macOS 15.6 (Sequoia), ocorria o seguinte erro:

```
dyld[40116]: Library not loaded: /System/Library/Frameworks/Carbon.framework/Versions/A/Carbon
Reason: tried: '/System/Library/Frameworks/Carbon.framework/Versions/A/Carbon' (no such file)
```

## 🔍 Causa Raiz

O framework **Carbon** foi removido no macOS 15.6 (Sequoia). O PyInstaller com a flag `--windowed` tentava usar o Carbon para criar aplicações GUI, causando incompatibilidade.

## ✅ Solução Implementada

### 1. Removido `--windowed` do PyInstaller
- Substituído por `--console` para criar executável compatível
- O executável agora funciona sem depender do Carbon

### 2. Bundle .app Criado Manualmente
- Estrutura do bundle criada manualmente após o build
- Compatível com macOS moderno (10.15+)

### 3. Info.plist Atualizado
```xml
<key>LSMinimumSystemVersion</key>
<string>10.15</string>
<key>NSHighResolutionCapable</key>
<true/>
<key>NSRequiresAquaSystemAppearance</key>
<false/>
<key>NSSupportsAutomaticGraphicsSwitching</key>
<true/>
```

## 📋 Mudanças no Script de Build

### Antes:
```bash
python3 -m PyInstaller \
    --onedir \
    --windowed \  # ❌ Causava problema
    ...
```

### Depois:
```bash
python3 -m PyInstaller \
    --onedir \
    --console \  # ✅ Compatível
    ...
```

E após o build, criar bundle .app manualmente com estrutura compatível.

## ✅ Verificação

Para verificar que não há mais dependência do Carbon:

```bash
otool -L dist/ObjectDetection_RT-DETR.app/Contents/MacOS/ObjectDetection_RT-DETR | grep Carbon
```

**Resultado esperado**: Nenhuma saída (nenhuma dependência do Carbon)

## 🚀 Status

- ✅ Problema corrigido
- ✅ Executável testado
- ✅ Compatível com macOS 15.6 (Sequoia)
- ✅ Compatível com versões anteriores (10.15+)

## 📝 Notas

- A interface gráfica Tkinter funcionará normalmente
- Pode aparecer uma janela de terminal brevemente na inicialização (normal)
- O sistema funciona completamente sem o Carbon framework

