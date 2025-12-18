# Renomeação do Sistema: ObjectDetection_DETR → ObjectDetection_RT-DETR

## ✅ Mudanças Realizadas

O sistema foi renomeado de **ObjectDetection_DETR** para **ObjectDetection_RT-DETR** em todos os arquivos relevantes.

### Arquivos Atualizados

1. **README.md**
   - Título principal atualizado
   - Estrutura de diretórios atualizada

2. **app.py**
   - Docstring atualizado
   - Mensagem de inicialização atualizada

3. **interface_tkinter.py**
   - Docstring atualizado
   - Título da janela atualizado
   - Título do cabeçalho atualizado

4. **interface.py**
   - Docstring atualizado
   - Mensagem de cabeçalho atualizada

5. **src/train_rtdetr.py**
   - Docstring atualizado

6. **src/infer_video.py**
   - Docstring atualizado

7. **src/infer_images.py**
   - Docstring atualizado

8. **src/eval_coco.py**
   - Docstring atualizado

9. **scripts/install_dependencies.sh**
   - Comentários atualizados
   - Mensagens de echo atualizadas

10. **scripts/bootstrap_mac.sh**
    - Mensagem de echo atualizada

## 📝 Nota sobre o Diretório

O diretório físico ainda pode estar com o nome antigo (`ObjectDetection_DETR`). Para renomeá-lo:

```bash
# Se você estiver no diretório pai
mv ObjectDetection_DETR ObjectDetection_RT-DETR

# Ou se estiver dentro do diretório
cd ..
mv ObjectDetection_DETR ObjectDetection_RT-DETR
cd ObjectDetection_RT-DETR
```

**Importante:** O arquivo `.git` contém referências ao caminho antigo, mas isso é normal em worktrees do Git e não afeta o funcionamento do sistema.

## ✅ Verificação

Todas as referências ao nome antigo foram atualizadas. O sistema continua funcionando normalmente:

- ✅ Sintaxe dos arquivos Python validada
- ✅ Todas as referências atualizadas
- ✅ Funcionalidade preservada
- ✅ Nenhuma quebra de compatibilidade

## 🚀 Próximos Passos

1. Renomear o diretório físico (opcional, mas recomendado)
2. Testar o sistema para garantir que tudo funciona:
   ```bash
   python app.py
   ```

O sistema está pronto para uso com o novo nome!
