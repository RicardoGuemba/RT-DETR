#!/usr/bin/env python3
"""
Interface Tkinter moderna para ObjectDetection_RT-DETR
Gerencia treinamento, predição e download de dados.
Design moderno com estado da arte em UI/UX.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import subprocess
import sys
import os
from pathlib import Path
import json
from dotenv import load_dotenv
import time
import queue

# Carregar variáveis de ambiente
load_dotenv()

class ModernTkinterApp:
    """Aplicação Tkinter moderna com design estado da arte."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 ObjectDetection_RT-DETR - Interface de Gerenciamento")
        # Abrir em tamanho “pleno” (sem precisar ajustar manualmente)
        self._maximize_window(self.root, fallback_geometry="1200x800", minsize=(1000, 700))
        
        # Configurar estilo moderno
        self.setup_style()
        
        # Variáveis
        self.training_process = None
        self.inference_process = None
        self.preview_window = None
        
        # Criar interface
        self.create_widgets()
        
        # Verificar status inicial
        self.check_initial_status()
    
    def setup_style(self):
        """Configura estilo moderno."""
        style = ttk.Style()
        
        # Tema moderno
        try:
            style.theme_use('clam')
        except:
            pass
        
        # Configurar cores modernas
        self.bg_color = "#f5f5f5"
        self.primary_color = "#2196F3"
        self.success_color = "#4CAF50"
        self.warning_color = "#FF9800"
        self.error_color = "#F44336"
        self.text_color = "#212121"
        self.secondary_bg = "#ffffff"
        
        # Configurar estilo dos widgets
        style.configure("Title.TLabel", font=("Helvetica", 18, "bold"), foreground=self.text_color)
        style.configure("Heading.TLabel", font=("Helvetica", 12, "bold"), foreground=self.text_color)
        style.configure("Primary.TButton", font=("Helvetica", 10, "bold"))
        style.configure("Success.TButton", font=("Helvetica", 10, "bold"))
        
        self.root.configure(bg=self.bg_color)
    
    def create_widgets(self):
        """Cria widgets da interface."""
        # Container principal
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        title_frame = tk.Frame(main_container, bg=self.bg_color)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(
            title_frame,
            text="🚀 ObjectDetection_RT-DETR - Sistema de Detecção de Objetos",
            style="Title.TLabel"
        )
        title_label.pack()
        
        # Notebook (abas)
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Aba 1: Download Dataset
        self.create_download_tab()
        
        # Aba 2: Correção de Dataset
        self.create_dataset_fix_tab()
        
        # Aba 3: Treinamento
        self.create_training_tab()
        
        # Aba 3: Predição
        self.create_inference_tab()
        
        # Aba 4: Avaliação
        self.create_evaluation_tab()
        
        # Aba 5: Status
        self.create_status_tab()
        
        # Barra de status
        self.status_bar = tk.Label(
            main_container,
            text="Pronto",
            relief=tk.SUNKEN,
            anchor=tk.W,
            bg="#e0e0e0",
            font=("Helvetica", 9)
        )
        self.status_bar.pack(fill=tk.X, pady=(10, 0))
    
    def create_download_tab(self):
        """Cria aba de download."""
        download_frame = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(download_frame, text="📥 Download Dataset")
        
        # Container com scroll
        canvas = tk.Canvas(download_frame, bg=self.secondary_bg, highlightthickness=0)
        scrollbar = ttk.Scrollbar(download_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Título
        title = ttk.Label(
            scrollable_frame,
            text="Gerenciar Dataset",
            style="Heading.TLabel"
        )
        title.pack(pady=(0, 20))
        
        # Frame para opções de download
        download_options_frame = ttk.LabelFrame(scrollable_frame, text="Download do Dataset", padding=15)
        download_options_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Versão do dataset
        ttk.Label(download_options_frame, text="Versão do Dataset:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.version_var = tk.StringVar(value=os.getenv("ROBOFLOW_VERSION", "3"))
        version_spinbox = ttk.Spinbox(
            download_options_frame,
            from_=1,
            to=100,
            textvariable=self.version_var,
            width=10
        )
        version_spinbox.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        # URL Raw (opcional - só será pedida se SDK falhar)
        ttk.Label(download_options_frame, text="URL Raw (opcional):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.download_url_var = tk.StringVar()
        url_entry = ttk.Entry(download_options_frame, textvariable=self.download_url_var, width=50)
        url_entry.grid(row=1, column=1, columnspan=2, sticky=tk.W+tk.E, padx=5, pady=5)
        ttk.Label(
            download_options_frame,
            text="(Deixe vazio para tentar SDK primeiro. Cole apenas se SDK falhar)",
            font=("Helvetica", 8),
            foreground="gray"
        ).grid(row=2, column=1, sticky=tk.W, padx=5)
        
        # Opção para usar dataset existente (oculta por padrão)
        self.use_existing_var = tk.BooleanVar(value=False)
        existing_check = ttk.Checkbutton(
            download_options_frame,
            text="Usar dataset já baixado (em vez de baixar do Roboflow)",
            variable=self.use_existing_var,
            command=self.toggle_existing_dataset
        )
        existing_check.grid(row=3, column=0, columnspan=3, sticky=tk.W, padx=5, pady=10)
        
        # Frame para dataset existente (inicialmente oculto)
        self.existing_frame = ttk.LabelFrame(scrollable_frame, text="Dataset Existente", padding=15)
        
        ttk.Label(self.existing_frame, text="Caminho:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.existing_dataset_var = tk.StringVar(value="")
        existing_entry = ttk.Entry(self.existing_frame, textvariable=self.existing_dataset_var, width=50)
        existing_entry.grid(row=0, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        ttk.Button(
            self.existing_frame,
            text="📁",
            command=lambda: self.browse_directory(self.existing_dataset_var)
        ).grid(row=0, column=2, padx=5, pady=5)
        
        # Diretório de destino
        self.dataset_dest_frame = ttk.LabelFrame(scrollable_frame, text="Diretório de Destino", padding=15)
        self.dataset_dest_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(self.dataset_dest_frame, text="Salvar em:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.dataset_dest_var = tk.StringVar(value="dataset")
        dest_entry = ttk.Entry(self.dataset_dest_frame, textvariable=self.dataset_dest_var, width=50)
        dest_entry.grid(row=0, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        ttk.Button(
            self.dataset_dest_frame,
            text="📁",
            command=lambda: self.browse_directory(self.dataset_dest_var)
        ).grid(row=0, column=2, padx=5, pady=5)
        
        # Botões de ação
        buttons_frame = ttk.Frame(scrollable_frame)
        buttons_frame.pack(fill=tk.X, pady=(0, 20))
        
        download_btn = ttk.Button(
            buttons_frame,
            text="📥 Baixar/Carregar Dataset",
            command=self.download_dataset,
            style="Primary.TButton"
        )
        download_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        verify_btn = ttk.Button(
            buttons_frame,
            text="✅ Verificar Dataset",
            command=self.verify_dataset,
        )
        verify_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Área de log
        log_frame = ttk.LabelFrame(scrollable_frame, text="Log", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        self.download_log = scrolledtext.ScrolledText(
            log_frame,
            height=15,
            font=("Courier", 9),
            bg="#1e1e1e",
            fg="#d4d4d4",
            insertbackground="#ffffff"
        )
        self.download_log.pack(fill=tk.BOTH, expand=True)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_dataset_fix_tab(self):
        """Cria aba de correção de dataset."""
        fix_frame = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(fix_frame, text="🔧 Correção Dataset")
        
        # Container com scroll
        canvas = tk.Canvas(fix_frame, bg=self.bg_color)
        scrollbar = ttk.Scrollbar(fix_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Título
        title_frame = tk.Frame(scrollable_frame, bg=self.bg_color)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(
            title_frame,
            text="🔧 Análise e Correção de Dataset COCO",
            style="Heading.TLabel"
        )
        title_label.pack()
        
        desc_label = ttk.Label(
            title_frame,
            text="Analise problemas no dataset e corrija automaticamente categorias não usadas, IDs inconsistentes e outros problemas.",
            font=("Helvetica", 9),
            foreground="gray",
            wraplength=800
        )
        desc_label.pack(pady=(5, 0))
        
        # Seleção de Dataset
        dataset_frame = ttk.LabelFrame(scrollable_frame, text="Seleção de Dataset", padding=15)
        dataset_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(dataset_frame, text="Diretório do Dataset:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.fix_dataset_dir_var = tk.StringVar(value="dataset")
        dataset_entry = ttk.Entry(dataset_frame, textvariable=self.fix_dataset_dir_var, width=50)
        dataset_entry.grid(row=0, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        ttk.Button(
            dataset_frame,
            text="📁",
            command=lambda: self.browse_directory(self.fix_dataset_dir_var)
        ).grid(row=0, column=2, padx=5, pady=5)
        
        dataset_frame.columnconfigure(1, weight=1)
        
        # Botões de Ação
        actions_frame = ttk.Frame(scrollable_frame)
        actions_frame.pack(fill=tk.X, pady=(0, 20))
        
        analyze_btn = ttk.Button(
            actions_frame,
            text="📊 Analisar Dataset",
            command=self.analyze_dataset,
            style="Primary.TButton"
        )
        analyze_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        fix_btn = ttk.Button(
            actions_frame,
            text="🔧 Corrigir Automaticamente",
            command=self.fix_dataset,
            style="Success.TButton"
        )
        fix_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        validate_btn = ttk.Button(
            actions_frame,
            text="✅ Validar Estrutura",
            command=self.validate_dataset_structure
        )
        validate_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Painel de Resultados (duas colunas)
        results_panel = tk.PanedWindow(scrollable_frame, orient=tk.HORIZONTAL, sashwidth=5)
        results_panel.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Coluna Esquerda: Estatísticas
        stats_frame = ttk.LabelFrame(results_panel, text="📊 Estatísticas do Dataset", padding=15)
        results_panel.add(stats_frame, width=400)
        
        self.stats_text = scrolledtext.ScrolledText(
            stats_frame,
            height=20,
            font=("Courier", 9),
            bg="#ffffff",
            fg="#000000",
            wrap=tk.WORD
        )
        self.stats_text.pack(fill=tk.BOTH, expand=True)
        
        # Coluna Direita: Problemas Detectados
        problems_frame = ttk.LabelFrame(results_panel, text="⚠️ Problemas Detectados", padding=15)
        results_panel.add(problems_frame, width=400)
        
        self.problems_text = scrolledtext.ScrolledText(
            problems_frame,
            height=20,
            font=("Courier", 9),
            bg="#fff3cd",
            fg="#856404",
            wrap=tk.WORD
        )
        self.problems_text.pack(fill=tk.BOTH, expand=True)
        
        # Área de Log
        log_frame = ttk.LabelFrame(scrollable_frame, text="📝 Log de Operações", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        self.fix_log = scrolledtext.ScrolledText(
            log_frame,
            height=10,
            font=("Courier", 9),
            bg="#1e1e1e",
            fg="#d4d4d4",
            insertbackground="#ffffff"
        )
        self.fix_log.pack(fill=tk.BOTH, expand=True)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def analyze_dataset(self):
        """Analisa o dataset e mostra estatísticas."""
        dataset_dir = Path(self.fix_dataset_dir_var.get())
        
        if not dataset_dir.exists():
            messagebox.showerror("Erro", f"Diretório não encontrado: {dataset_dir}")
            return
        
        self.log_message(self.fix_log, f"🔍 Analisando dataset em: {dataset_dir}")
        self.update_status_bar("Analisando dataset...")
        
        def analyze_thread():
            try:
                from collections import Counter
                
                stats_lines = []
                problems_lines = []
                
                splits = ["train", "valid", "test"]
                all_category_ids = set()
                all_categories = {}
                
                for split in splits:
                    json_file = dataset_dir / f"{split}/_annotations.coco.json"
                    
                    if not json_file.exists():
                        stats_lines.append(f"\n❌ {split.upper()}: Arquivo não encontrado")
                        problems_lines.append(f"⚠️  {split.upper()}: Arquivo _annotations.coco.json não encontrado")
                        continue
                    
                    try:
                        with open(json_file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        
                        # Estatísticas básicas
                        n_images = len(data.get("images", []))
                        n_annotations = len(data.get("annotations", []))
                        categories = data.get("categories", [])
                        
                        stats_lines.append(f"\n{'='*60}")
                        stats_lines.append(f"📁 {split.upper()}")
                        stats_lines.append(f"{'='*60}")
                        stats_lines.append(f"  Imagens: {n_images}")
                        stats_lines.append(f"  Anotações: {n_annotations}")
                        stats_lines.append(f"  Categorias definidas: {len(categories)}")
                        
                        # Mapear categorias
                        cat_map = {cat["id"]: cat.get("name", "???") for cat in categories}
                        all_categories.update(cat_map)
                        
                        # Contar anotações por categoria
                        if n_annotations > 0:
                            cat_counter = Counter(ann["category_id"] for ann in data.get("annotations", []))
                            stats_lines.append(f"\n  Anotações por categoria:")
                            
                            used_cats = set()
                            for cat_id, count in sorted(cat_counter.items()):
                                cat_name = cat_map.get(cat_id, f"ID {cat_id} (não encontrado)")
                                stats_lines.append(f"    • {cat_name} (ID: {cat_id}): {count} anotações")
                                used_cats.add(cat_id)
                                all_category_ids.add(cat_id)
                            
                            # Verificar categorias não usadas
                            defined_cat_ids = {cat["id"] for cat in categories}
                            unused_cats = defined_cat_ids - used_cats
                            
                            if unused_cats:
                                problems_lines.append(f"\n⚠️  {split.upper()}: {len(unused_cats)} categoria(s) definida(s) mas não usada(s):")
                                for cat_id in sorted(unused_cats):
                                    cat_name = cat_map.get(cat_id, f"ID {cat_id}")
                                    problems_lines.append(f"    • {cat_name} (ID: {cat_id})")
                            
                            # Verificar IDs inconsistentes
                            if used_cats and max(used_cats) >= len(categories):
                                problems_lines.append(f"\n⚠️  {split.upper()}: IDs de categoria podem estar inconsistentes")
                                problems_lines.append(f"    Maior ID usado: {max(used_cats)}, Total de categorias: {len(categories)}")
                        else:
                            problems_lines.append(f"\n⚠️  {split.upper()}: Nenhuma anotação encontrada!")
                    
                    except json.JSONDecodeError as e:
                        problems_lines.append(f"\n❌ {split.upper()}: Erro ao ler JSON: {e}")
                    except Exception as e:
                        problems_lines.append(f"\n❌ {split.upper()}: Erro: {e}")
                
                # Resumo geral
                stats_lines.append(f"\n{'='*60}")
                stats_lines.append("📊 RESUMO GERAL")
                stats_lines.append(f"{'='*60}")
                stats_lines.append(f"  Total de categorias únicas encontradas: {len(all_category_ids)}")
                stats_lines.append(f"  Categorias definidas em todos os splits: {len(all_categories)}")
                
                # Detectar se há apenas 1 classe real
                is_single_class = len(all_category_ids) == 1
                
                if all_category_ids:
                    stats_lines.append(f"\n  IDs de categoria usados: {sorted(all_category_ids)}")
                    
                    if is_single_class:
                        # Caso especial: apenas 1 classe
                        used_id = list(all_category_ids)[0]
                        cat_name = all_categories.get(used_id, "desconhecida")
                        
                        stats_lines.append(f"\n  🎯 DETECÇÃO: Dataset tem APENAS 1 CLASSE REAL")
                        stats_lines.append(f"     Classe: '{cat_name}' (ID atual: {used_id})")
                        
                        if used_id != 0:
                            problems_lines.append(f"\n⚠️  PROBLEMA: Dataset tem 1 classe mas category_id={used_id} (deveria ser 0)")
                            problems_lines.append(f"    Impacto: Modelo será configurado com num_labels=1, mas IDs inconsistentes")
                            problems_lines.append(f"    Correção: Remapear category_id para 0 em todas as anotações")
                            problems_lines.append(f"    Recomendação: Use 'Corrigir Automaticamente' para normalizar")
                        else:
                            stats_lines.append(f"     ✅ ID já está correto (0)")
                            stats_lines.append(f"\n  💡 CONFIGURAÇÃO RECOMENDADA:")
                            stats_lines.append(f"     • num_labels = 1")
                            stats_lines.append(f"     • CLASS_NAMES = ['{cat_name}']")
                            stats_lines.append(f"     • Modelo detectará: '{cat_name}' vs fundo")
                    else:
                        # Múltiplas classes
                        if max(all_category_ids) >= len(all_categories):
                            problems_lines.append(f"\n⚠️  PROBLEMA CRÍTICO: IDs não começam em 0 ou não são contíguos")
                            problems_lines.append(f"    Maior ID: {max(all_category_ids)}, Total de categorias: {len(all_categories)}")
                            problems_lines.append(f"    Recomendação: Remapear IDs para 0..N-1")
                        
                        stats_lines.append(f"\n  💡 CONFIGURAÇÃO RECOMENDADA:")
                        stats_lines.append(f"     • num_labels = {len(all_category_ids)}")
                        class_names = [all_categories.get(cid, f"classe_{cid}") for cid in sorted(all_category_ids)]
                        stats_lines.append(f"     • CLASS_NAMES = {class_names}")
                
                # Atualizar UI
                self.stats_text.delete(1.0, tk.END)
                self.stats_text.insert(1.0, "\n".join(stats_lines))
                
                self.problems_text.delete(1.0, tk.END)
                if problems_lines:
                    self.problems_text.insert(1.0, "\n".join(problems_lines))
                else:
                    self.problems_text.insert(1.0, "✅ Nenhum problema detectado!")
                
                self.log_message(self.fix_log, "\n✅ Análise concluída!")
                self.update_status_bar("Análise concluída!")
                
            except Exception as e:
                self.log_message(self.fix_log, f"\n❌ Erro na análise: {e}")
                messagebox.showerror("Erro", f"Erro ao analisar dataset: {e}")
        
        threading.Thread(target=analyze_thread, daemon=True).start()
    
    def fix_dataset(self):
        """Corrige problemas no dataset automaticamente."""
        dataset_dir = Path(self.fix_dataset_dir_var.get())
        
        if not dataset_dir.exists():
            messagebox.showerror("Erro", f"Diretório não encontrado: {dataset_dir}")
            return
        
        resposta = messagebox.askyesno(
            "Confirmar Correção",
            "Isso irá modificar os arquivos JSON do dataset.\n"
            "Recomendado fazer backup antes.\n\n"
            "Deseja continuar?"
        )
        
        if not resposta:
            return
        
        self.log_message(self.fix_log, f"🔧 Iniciando correção automática...")
        self.update_status_bar("Corrigindo dataset...")
        
        def fix_thread():
            try:
                import sys
                from collections import Counter
                sys.path.insert(0, str(Path(__file__).parent / "src"))
                from coco_utils import remap_category_ids, load_coco_json
                
                splits = ["train", "valid", "test"]
                fixed_count = 0
                
                # Primeiro, detectar se há apenas 1 classe em todos os splits
                all_used_cats = set()
                for split in splits:
                    json_file = dataset_dir / f"{split}/_annotations.coco.json"
                    if json_file.exists():
                        try:
                            data = load_coco_json(json_file)
                            used_cats = {ann["category_id"] for ann in data.get("annotations", [])}
                            all_used_cats.update(used_cats)
                        except:
                            pass
                
                is_single_class = len(all_used_cats) == 1
                
                if is_single_class:
                    self.log_message(self.fix_log, f"  🎯 Detectado: Dataset tem apenas 1 classe real")
                    self.log_message(self.fix_log, f"     Garantindo category_id=0 para consistência")
                
                for split in splits:
                    json_file = dataset_dir / f"{split}/_annotations.coco.json"
                    
                    if not json_file.exists():
                        self.log_message(self.fix_log, f"  ⏭️  {split}: Arquivo não encontrado, pulando...")
                        continue
                    
                    try:
                        # Carregar dados
                        coco_data = load_coco_json(json_file)
                        
                        # Remapear IDs (remove categorias não usadas e normaliza IDs)
                        coco_data_fixed, id_mapping = remap_category_ids(coco_data)
                        
                        # Se há apenas 1 classe, garantir que seja id=0
                        if is_single_class and len(coco_data_fixed.get("categories", [])) == 1:
                            # Forçar categoria única para id=0
                            used_cat = coco_data_fixed["categories"][0]
                            cat_name = used_cat.get("name", "embalagem")
                            
                            # Se o id não é 0, corrigir
                            if used_cat["id"] != 0:
                                self.log_message(self.fix_log, f"  🔧 {split}: Corrigindo category_id {used_cat['id']} → 0")
                                used_cat["id"] = 0
                                
                                # Remapear todas as anotações para 0
                                for ann in coco_data_fixed["annotations"]:
                                    ann["category_id"] = 0
                                
                                id_mapping = {old_id: 0 for old_id in id_mapping.keys()}
                            
                            # Garantir que há apenas 1 categoria com id=0
                            coco_data_fixed["categories"] = [{"id": 0, "name": cat_name, "supercategory": used_cat.get("supercategory", "none")}]
                        
                        # Verificar se houve mudanças
                        original_cats = len(coco_data.get("categories", []))
                        fixed_cats = len(coco_data_fixed.get("categories", []))
                        original_ids = {cat["id"] for cat in coco_data.get("categories", [])}
                        fixed_ids = {cat["id"] for cat in coco_data_fixed.get("categories", [])}
                        
                        if original_cats != fixed_cats or id_mapping or original_ids != fixed_ids:
                            # Fazer backup
                            backup_file = json_file.with_suffix('.coco.json.backup')
                            import shutil
                            shutil.copy2(json_file, backup_file)
                            self.log_message(self.fix_log, f"  💾 {split}: Backup criado em {backup_file.name}")
                            
                            # Salvar arquivo corrigido
                            with open(json_file, 'w', encoding='utf-8') as f:
                                json.dump(coco_data_fixed, f, indent=2, ensure_ascii=False)
                            
                            self.log_message(self.fix_log, f"  ✅ {split}: Corrigido!")
                            self.log_message(self.fix_log, f"     Categorias: {original_cats} → {fixed_cats}")
                            if id_mapping:
                                self.log_message(self.fix_log, f"     Mapeamento: {id_mapping}")
                            
                            if is_single_class:
                                self.log_message(self.fix_log, f"     ✅ Garantido: category_id=0 para classe única")
                            
                            fixed_count += 1
                        else:
                            self.log_message(self.fix_log, f"  ✓ {split}: Já está correto, nenhuma alteração necessária")
                    
                    except Exception as e:
                        self.log_message(self.fix_log, f"  ❌ {split}: Erro - {e}")
                        import traceback
                        self.log_message(self.fix_log, traceback.format_exc())
                
                if fixed_count > 0:
                    self.log_message(self.fix_log, f"\n✅ Correção concluída! {fixed_count} split(s) corrigido(s)")
                    self.log_message(self.fix_log, f"💡 Recomendado: Execute 'Analisar Dataset' novamente para verificar")
                    messagebox.showinfo(
                        "Sucesso",
                        f"Dataset corrigido com sucesso!\n\n"
                        f"{fixed_count} split(s) foram corrigidos.\n"
                        f"Backups foram criados com extensão .backup"
                    )
                else:
                    self.log_message(self.fix_log, f"\n✅ Nenhuma correção necessária!")
                    messagebox.showinfo("Info", "Dataset já está correto, nenhuma alteração foi feita.")
                
                self.update_status_bar("Correção concluída!")
                
            except Exception as e:
                self.log_message(self.fix_log, f"\n❌ Erro na correção: {e}")
                import traceback
                self.log_message(self.fix_log, traceback.format_exc())
                messagebox.showerror("Erro", f"Erro ao corrigir dataset: {e}")
        
        threading.Thread(target=fix_thread, daemon=True).start()
    
    def validate_dataset_structure(self):
        """Valida estrutura COCO do dataset."""
        dataset_dir = Path(self.fix_dataset_dir_var.get())
        
        if not dataset_dir.exists():
            messagebox.showerror("Erro", f"Diretório não encontrado: {dataset_dir}")
            return
        
        self.log_message(self.fix_log, f"✅ Validando estrutura COCO...")
        self.update_status_bar("Validando estrutura...")
        
        def validate_thread():
            try:
                validation_results = []
                splits = ["train", "valid", "test"]
                
                for split in splits:
                    json_file = dataset_dir / f"{split}/_annotations.coco.json"
                    image_dir = dataset_dir / split
                    
                    if not json_file.exists():
                        validation_results.append(f"❌ {split.upper()}: Arquivo JSON não encontrado")
                        continue
                    
                    try:
                        with open(json_file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        
                        # Validar estrutura básica
                        required_keys = ["images", "annotations", "categories"]
                        missing_keys = [k for k in required_keys if k not in data]
                        
                        if missing_keys:
                            validation_results.append(f"❌ {split.upper()}: Chaves faltando: {missing_keys}")
                            continue
                        
                        # Validar imagens
                        images = data.get("images", [])
                        annotations = data.get("annotations", [])
                        categories = data.get("categories", [])
                        
                        validation_results.append(f"\n✅ {split.upper()}:")
                        validation_results.append(f"   Estrutura JSON: OK")
                        validation_results.append(f"   Imagens: {len(images)}")
                        validation_results.append(f"   Anotações: {len(annotations)}")
                        validation_results.append(f"   Categorias: {len(categories)}")
                        
                        # Validar referências de imagens
                        image_ids = {img["id"] for img in images}
                        ann_image_ids = {ann["image_id"] for ann in annotations}
                        missing_refs = ann_image_ids - image_ids
                        
                        if missing_refs:
                            validation_results.append(f"   ⚠️  {len(missing_refs)} anotação(ões) referenciam imagem(s) inexistente(s)")
                        else:
                            validation_results.append(f"   Referências de imagens: OK")
                        
                        # Validar referências de categorias
                        cat_ids = {cat["id"] for cat in categories}
                        ann_cat_ids = {ann["category_id"] for ann in annotations}
                        missing_cats = ann_cat_ids - cat_ids
                        
                        if missing_cats:
                            validation_results.append(f"   ⚠️  {len(missing_cats)} anotação(ões) referenciam categoria(s) inexistente(s): {sorted(missing_cats)}")
                        else:
                            validation_results.append(f"   Referências de categorias: OK")
                        
                        # Validar arquivos de imagem
                        if image_dir.exists():
                            image_files = set(f.name for f in image_dir.iterdir() if f.suffix.lower() in ['.jpg', '.jpeg', '.png'])
                            json_image_files = {img["file_name"] for img in images}
                            missing_files = json_image_files - image_files
                            
                            if missing_files:
                                validation_results.append(f"   ⚠️  {len(missing_files)} imagem(ns) referenciada(s) no JSON não encontrada(s) no diretório")
                            else:
                                validation_results.append(f"   Arquivos de imagem: OK")
                    
                    except json.JSONDecodeError as e:
                        validation_results.append(f"❌ {split.upper()}: JSON inválido - {e}")
                    except Exception as e:
                        validation_results.append(f"❌ {split.upper()}: Erro - {e}")
                
                # Atualizar UI
                self.stats_text.delete(1.0, tk.END)
                self.stats_text.insert(1.0, "\n".join(validation_results))
                
                self.log_message(self.fix_log, "\n✅ Validação concluída!")
                self.update_status_bar("Validação concluída!")
                
            except Exception as e:
                self.log_message(self.fix_log, f"\n❌ Erro na validação: {e}")
                messagebox.showerror("Erro", f"Erro ao validar dataset: {e}")
        
        threading.Thread(target=validate_thread, daemon=True).start()
    
    def create_training_tab(self):
        """Cria aba de treinamento."""
        training_frame = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(training_frame, text="🏋️ Treinamento")
        
        # Container principal
        main_panel = tk.PanedWindow(training_frame, orient=tk.HORIZONTAL, sashwidth=5)
        main_panel.pack(fill=tk.BOTH, expand=True)
        
        # Painel esquerdo: Parâmetros (com scroll)
        left_panel = ttk.Frame(main_panel, padding=15)
        main_panel.add(left_panel, width=450)
        
        # Container com scroll para parâmetros
        canvas_params = tk.Canvas(left_panel, bg=self.bg_color, highlightthickness=0)
        scrollbar_params = ttk.Scrollbar(left_panel, orient="vertical", command=canvas_params.yview)
        scrollable_params = ttk.Frame(canvas_params)
        
        scrollable_params.bind(
            "<Configure>",
            lambda e: canvas_params.configure(scrollregion=canvas_params.bbox("all"))
        )
        
        canvas_params.create_window((0, 0), window=scrollable_params, anchor="nw")
        canvas_params.configure(yscrollcommand=scrollbar_params.set)
        
        # Título
        title = ttk.Label(scrollable_params, text="Hiperparâmetros de Treinamento", style="Heading.TLabel")
        title.pack(pady=(0, 20))
        
        # Formulário de parâmetros básicos
        params_frame = ttk.LabelFrame(scrollable_params, text="Parâmetros Básicos", padding=15)
        params_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Épocas
        ttk.Label(params_frame, text="Épocas:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=8)
        self.epochs_var = tk.StringVar(value="50")
        epochs_entry = ttk.Entry(params_frame, textvariable=self.epochs_var, width=15)
        epochs_entry.grid(row=0, column=1, padx=5, pady=8)
        ttk.Label(params_frame, text="(1-1000)", font=("Helvetica", 8), foreground="gray").grid(row=0, column=2, padx=5)
        
        # Batch Size
        ttk.Label(params_frame, text="Batch Size:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=8)
        self.batch_size_var = tk.StringVar(value="1")
        batch_size_entry = ttk.Entry(params_frame, textvariable=self.batch_size_var, width=15)
        batch_size_entry.grid(row=1, column=1, padx=5, pady=8)
        ttk.Label(params_frame, text="(1-16)", font=("Helvetica", 8), foreground="gray").grid(row=1, column=2, padx=5)
        
        # Tamanho da Imagem
        ttk.Label(params_frame, text="Tamanho da Imagem:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=8)
        self.img_size_var = tk.StringVar(value="640")
        img_size_combo = ttk.Combobox(
            params_frame,
            textvariable=self.img_size_var,
            values=["640", "832", "960"],
            width=12,
            state="readonly"
        )
        img_size_combo.grid(row=2, column=1, padx=5, pady=8)
        
        # Learning Rate
        ttk.Label(params_frame, text="Learning Rate:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=8)
        self.learning_rate_var = tk.StringVar(value="1e-5")
        lr_entry = ttk.Entry(params_frame, textvariable=self.learning_rate_var, width=15)
        lr_entry.grid(row=3, column=1, padx=5, pady=8)
        ttk.Label(params_frame, text="(ex: 1e-5)", font=("Helvetica", 8), foreground="gray").grid(row=3, column=2, padx=5)
        
        # Gradient Accumulation
        ttk.Label(params_frame, text="Gradient Accumulation:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=8)
        self.gradient_accum_var = tk.StringVar(value="4")
        grad_accum_entry = ttk.Entry(params_frame, textvariable=self.gradient_accum_var, width=15)
        grad_accum_entry.grid(row=4, column=1, padx=5, pady=8)
        ttk.Label(params_frame, text="(1-32)", font=("Helvetica", 8), foreground="gray").grid(row=4, column=2, padx=5)
        
        # Save Steps
        ttk.Label(params_frame, text="Save Steps:").grid(row=5, column=0, sticky=tk.W, padx=5, pady=8)
        self.save_steps_var = tk.StringVar(value="500")
        save_steps_entry = ttk.Entry(params_frame, textvariable=self.save_steps_var, width=15)
        save_steps_entry.grid(row=5, column=1, padx=5, pady=8)
        
        # Eval Steps
        ttk.Label(params_frame, text="Eval Steps:").grid(row=6, column=0, sticky=tk.W, padx=5, pady=8)
        self.eval_steps_var = tk.StringVar(value="500")
        eval_steps_entry = ttk.Entry(params_frame, textvariable=self.eval_steps_var, width=15)
        eval_steps_entry.grid(row=6, column=1, padx=5, pady=8)
        
        # Parâmetros avançados de otimização
        adv_params_frame = ttk.LabelFrame(scrollable_params, text="Parâmetros Avançados de Otimização", padding=15)
        adv_params_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Weight Decay
        ttk.Label(adv_params_frame, text="Weight Decay:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=8)
        self.weight_decay_var = tk.StringVar(value="0.0001")
        weight_decay_entry = ttk.Entry(adv_params_frame, textvariable=self.weight_decay_var, width=15)
        weight_decay_entry.grid(row=0, column=1, padx=5, pady=8)
        ttk.Label(adv_params_frame, text="(ex: 0.0001)", font=("Helvetica", 8), foreground="gray").grid(row=0, column=2, padx=5)
        
        # Warmup Steps
        ttk.Label(adv_params_frame, text="Warmup Steps:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=8)
        self.warmup_steps_var = tk.StringVar(value="500")
        warmup_steps_entry = ttk.Entry(adv_params_frame, textvariable=self.warmup_steps_var, width=15)
        warmup_steps_entry.grid(row=1, column=1, padx=5, pady=8)
        
        # Warmup Ratio (alternativa)
        ttk.Label(adv_params_frame, text="Warmup Ratio:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=8)
        self.warmup_ratio_var = tk.StringVar(value="")
        warmup_ratio_entry = ttk.Entry(adv_params_frame, textvariable=self.warmup_ratio_var, width=15)
        warmup_ratio_entry.grid(row=2, column=1, padx=5, pady=8)
        ttk.Label(adv_params_frame, text="(opcional, 0.0-1.0)", font=("Helvetica", 8), foreground="gray").grid(row=2, column=2, padx=5)
        
        # LR Scheduler Type
        ttk.Label(adv_params_frame, text="LR Scheduler:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=8)
        self.lr_scheduler_var = tk.StringVar(value="cosine")
        lr_scheduler_combo = ttk.Combobox(
            adv_params_frame,
            textvariable=self.lr_scheduler_var,
            values=["linear", "cosine", "cosine_with_restarts", "polynomial", "constant", "constant_with_warmup"],
            width=12,
            state="readonly"
        )
        lr_scheduler_combo.grid(row=3, column=1, padx=5, pady=8)
        
        # Adam Beta1
        ttk.Label(adv_params_frame, text="Adam Beta1:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=8)
        self.adam_beta1_var = tk.StringVar(value="0.9")
        adam_beta1_entry = ttk.Entry(adv_params_frame, textvariable=self.adam_beta1_var, width=15)
        adam_beta1_entry.grid(row=4, column=1, padx=5, pady=8)
        
        # Adam Beta2
        ttk.Label(adv_params_frame, text="Adam Beta2:").grid(row=5, column=0, sticky=tk.W, padx=5, pady=8)
        self.adam_beta2_var = tk.StringVar(value="0.999")
        adam_beta2_entry = ttk.Entry(adv_params_frame, textvariable=self.adam_beta2_var, width=15)
        adam_beta2_entry.grid(row=5, column=1, padx=5, pady=8)
        
        # Adam Epsilon
        ttk.Label(adv_params_frame, text="Adam Epsilon:").grid(row=6, column=0, sticky=tk.W, padx=5, pady=8)
        self.adam_epsilon_var = tk.StringVar(value="1e-8")
        adam_epsilon_entry = ttk.Entry(adv_params_frame, textvariable=self.adam_epsilon_var, width=15)
        adam_epsilon_entry.grid(row=6, column=1, padx=5, pady=8)
        
        # Max Grad Norm
        ttk.Label(adv_params_frame, text="Max Grad Norm:").grid(row=7, column=0, sticky=tk.W, padx=5, pady=8)
        self.max_grad_norm_var = tk.StringVar(value="1.0")
        max_grad_norm_entry = ttk.Entry(adv_params_frame, textvariable=self.max_grad_norm_var, width=15)
        max_grad_norm_entry.grid(row=7, column=1, padx=5, pady=8)
        
        # FP16
        self.fp16_var = tk.BooleanVar(value=False)
        fp16_check = ttk.Checkbutton(
            adv_params_frame,
            text="Usar FP16 (acelera treinamento, não suportado em MPS)",
            variable=self.fp16_var
        )
        fp16_check.grid(row=8, column=0, columnspan=3, sticky=tk.W, padx=5, pady=8)
        
        # Diretórios
        dirs_frame = ttk.LabelFrame(scrollable_params, text="Diretórios", padding=15)
        dirs_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(dirs_frame, text="Dataset:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.dataset_dir_var = tk.StringVar(value="dataset")
        ttk.Entry(dirs_frame, textvariable=self.dataset_dir_var, width=25).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(dirs_frame, text="📁", command=lambda: self.browse_directory(self.dataset_dir_var)).grid(row=0, column=2, padx=5)
        
        ttk.Label(dirs_frame, text="Output:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.output_dir_var = tk.StringVar(value="runs_rtdetr")
        ttk.Entry(dirs_frame, textvariable=self.output_dir_var, width=25).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(dirs_frame, text="📁", command=lambda: self.browse_directory(self.output_dir_var)).grid(row=1, column=2, padx=5)
        
        # Botões de ação
        buttons_frame = ttk.Frame(scrollable_params)
        buttons_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Pack canvas e scrollbar
        canvas_params.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_params.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.train_btn = ttk.Button(
            buttons_frame,
            text="🚀 Iniciar Treinamento",
            command=self.start_training,
            style="Primary.TButton"
        )
        self.train_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        self.stop_train_btn = ttk.Button(
            buttons_frame,
            text="⏹️ Parar",
            command=self.stop_training,
            state=tk.DISABLED
        )
        self.stop_train_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Painel direito: Log
        right_panel = ttk.Frame(main_panel, padding=15)
        main_panel.add(right_panel)
        
        log_title = ttk.Label(right_panel, text="Log de Treinamento", style="Heading.TLabel")
        log_title.pack(pady=(0, 10))
        
        self.training_log = scrolledtext.ScrolledText(
            right_panel,
            height=30,
            font=("Courier", 9),
            bg="#1e1e1e",
            fg="#d4d4d4",
            insertbackground="#ffffff"
        )
        self.training_log.pack(fill=tk.BOTH, expand=True)
    
    def create_inference_tab(self):
        """Cria aba de predição."""
        inference_frame = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(inference_frame, text="🔮 Predição")
        
        # Container principal: Configurações | Log
        main_panel = tk.PanedWindow(inference_frame, orient=tk.HORIZONTAL, sashwidth=5)
        main_panel.pack(fill=tk.BOTH, expand=True)
        
        # Painel esquerdo: Configurações
        left_panel = ttk.Frame(main_panel, padding=15)
        main_panel.add(left_panel, width=400)
        
        title = ttk.Label(left_panel, text="Configurações de Predição", style="Heading.TLabel")
        title.pack(pady=(0, 20))
        
        # Seleção de modelo
        model_frame = ttk.LabelFrame(left_panel, text="Modelo", padding=15)
        model_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(model_frame, text="Modelo:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.model_choice_var = tk.StringVar(value="model_best")
        model_combo = ttk.Combobox(
            model_frame,
            textvariable=self.model_choice_var,
            values=["model_best", "model_final"],
            width=20,
            state="readonly"
        )
        model_combo.grid(row=0, column=1, padx=5, pady=5)
        
        # Parâmetros de predição
        params_frame = ttk.LabelFrame(left_panel, text="Parâmetros de Detecção", padding=15)
        params_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Score Threshold
        ttk.Label(params_frame, text="Score Threshold:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=8)
        self.score_threshold_var = tk.DoubleVar(value=0.8)
        score_scale = ttk.Scale(
            params_frame,
            from_=0.0,
            to=1.0,
            variable=self.score_threshold_var,
            orient=tk.HORIZONTAL,
            length=200
        )
        score_scale.grid(row=0, column=1, padx=5, pady=8)
        self.score_threshold_label = ttk.Label(params_frame, text="0.80")
        self.score_threshold_label.grid(row=0, column=2, padx=5)
        score_scale.configure(command=lambda v: self.score_threshold_label.config(text=f"{float(v):.2f}"))
        
        # IOU Threshold
        ttk.Label(params_frame, text="IOU Threshold:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=8)
        self.iou_threshold_var = tk.DoubleVar(value=0.5)
        iou_scale = ttk.Scale(
            params_frame,
            from_=0.0,
            to=1.0,
            variable=self.iou_threshold_var,
            orient=tk.HORIZONTAL,
            length=200
        )
        iou_scale.grid(row=1, column=1, padx=5, pady=8)
        self.iou_threshold_label = ttk.Label(params_frame, text="0.50")
        self.iou_threshold_label.grid(row=1, column=2, padx=5)
        iou_scale.configure(command=lambda v: self.iou_threshold_label.config(text=f"{float(v):.2f}"))
        
        # Max Detections
        ttk.Label(params_frame, text="Max Detections:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=8)
        self.max_detections_var = tk.StringVar(value="100")
        max_det_entry = ttk.Entry(params_frame, textvariable=self.max_detections_var, width=15)
        max_det_entry.grid(row=2, column=1, padx=5, pady=8)
        
        # Preview em tempo real (apenas para vídeo)
        self.show_preview_var = tk.BooleanVar(value=False)
        self.preview_check = ttk.Checkbutton(
            params_frame,
            text="📺 Exibir preview em tempo real (velocidade do vídeo)",
            variable=self.show_preview_var,
            state=tk.DISABLED,  # Inicialmente desabilitado até selecionar vídeo
            command=self.toggle_preview_panel
        )
        self.preview_check.grid(row=3, column=0, columnspan=3, sticky=tk.W, padx=5, pady=8)
        
        # Tipo de entrada
        input_type_frame = ttk.LabelFrame(left_panel, text="Tipo de Entrada", padding=15)
        input_type_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.inference_input_type_var = tk.StringVar(value="directory")
        ttk.Radiobutton(
            input_type_frame,
            text="📁 Pasta de Imagens",
            variable=self.inference_input_type_var,
            value="directory",
            command=self.update_inference_input_ui
        ).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        ttk.Radiobutton(
            input_type_frame,
            text="🖼️  Imagem Única",
            variable=self.inference_input_type_var,
            value="image",
            command=self.update_inference_input_ui
        ).grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Radiobutton(
            input_type_frame,
            text="📹 Vídeo",
            variable=self.inference_input_type_var,
            value="video",
            command=self.update_inference_input_ui
        ).grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        
        # Diretórios/Arquivos
        dirs_frame = ttk.LabelFrame(left_panel, text="Entrada", padding=15)
        dirs_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(dirs_frame, text="Input:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.inference_input_var = tk.StringVar(value="dataset/test")
        self.inference_input_entry = ttk.Entry(dirs_frame, textvariable=self.inference_input_var, width=25)
        self.inference_input_entry.grid(row=0, column=1, padx=5, pady=5)
        self.inference_browse_btn = ttk.Button(
            dirs_frame,
            text="📁",
            command=self.browse_inference_input
        )
        self.inference_browse_btn.grid(row=0, column=2, padx=5)
        
        ttk.Label(dirs_frame, text="Output:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.inference_output_var = tk.StringVar(value="runs_rtdetr/infer_out")
        ttk.Entry(dirs_frame, textvariable=self.inference_output_var, width=25).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(dirs_frame, text="📁", command=lambda: self.browse_directory(self.inference_output_var)).grid(row=1, column=2, padx=5)
        
        # Atualizar UI inicialmente
        self.update_inference_input_ui()
        
        # Botões
        buttons_frame = ttk.Frame(left_panel)
        buttons_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.inference_btn = ttk.Button(
            buttons_frame,
            text="🔮 Executar Predição",
            command=self.start_inference,
            style="Primary.TButton"
        )
        self.inference_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        self.stop_inference_btn = ttk.Button(
            buttons_frame,
            text="⏹️ Parar",
            command=self.stop_inference,
            state=tk.DISABLED
        )
        self.stop_inference_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Painel direito: Log
        right_panel = ttk.Frame(main_panel, padding=15)
        main_panel.add(right_panel)
        
        log_title = ttk.Label(right_panel, text="Log de Predição", style="Heading.TLabel")
        log_title.pack(pady=(0, 10))
        
        self.inference_log = scrolledtext.ScrolledText(
            right_panel,
            height=30,
            font=("Courier", 9),
            bg="#1e1e1e",
            fg="#d4d4d4",
            insertbackground="#ffffff"
        )
        self.inference_log.pack(fill=tk.BOTH, expand=True)
        
        # Variáveis para preview em tempo real
        self.preview_queue = None
        self.preview_thread = None
        self.preview_stop_event = None
    
    def create_evaluation_tab(self):
        """Cria aba de avaliação."""
        eval_frame = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(eval_frame, text="📊 Avaliação")
        
        title = ttk.Label(eval_frame, text="Avaliar Modelo Treinado", style="Heading.TLabel")
        title.pack(pady=(0, 20))
        
        # Configurações
        config_frame = ttk.LabelFrame(eval_frame, text="Configurações", padding=15)
        config_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(config_frame, text="Modelo:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.eval_model_var = tk.StringVar(value="model_best")
        ttk.Combobox(
            config_frame,
            textvariable=self.eval_model_var,
            values=["model_best", "model_final"],
            width=20,
            state="readonly"
        ).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(config_frame, text="Split:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.eval_split_var = tk.StringVar(value="valid")
        ttk.Combobox(
            config_frame,
            textvariable=self.eval_split_var,
            values=["train", "valid", "test"],
            width=20,
            state="readonly"
        ).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Button(
            config_frame,
            text="📊 Avaliar",
            command=self.start_evaluation,
            style="Primary.TButton"
        ).grid(row=2, column=0, columnspan=2, pady=10)
        
        # Log
        log_frame = ttk.LabelFrame(eval_frame, text="Resultados", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.eval_log = scrolledtext.ScrolledText(
            log_frame,
            height=25,
            font=("Courier", 9),
            bg="#1e1e1e",
            fg="#d4d4d4"
        )
        self.eval_log.pack(fill=tk.BOTH, expand=True)
    
    def create_status_tab(self):
        """Cria aba de status."""
        status_frame = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(status_frame, text="✅ Status")
        
        title = ttk.Label(status_frame, text="Status do Sistema", style="Heading.TLabel")
        title.pack(pady=(0, 20))
        
        # Botão de atualizar
        ttk.Button(
            status_frame,
            text="🔄 Atualizar Status",
            command=self.update_status
        ).pack(pady=(0, 20))
        
        # Área de status
        self.status_text = scrolledtext.ScrolledText(
            status_frame,
            height=30,
            font=("Courier", 10),
            bg="#ffffff",
            fg="#000000"
        )
        self.status_text.pack(fill=tk.BOTH, expand=True)
    
    def browse_directory(self, var):
        """Abre diálogo para selecionar diretório."""
        directory = filedialog.askdirectory(initialdir=var.get())
        if directory:
            var.set(directory)
    
    def browse_inference_input(self):
        """Abre diálogo para selecionar entrada (diretório, imagem ou vídeo)."""
        input_type = self.inference_input_type_var.get()
        
        if input_type == "directory":
            directory = filedialog.askdirectory(initialdir=self.inference_input_var.get())
            if directory:
                self.inference_input_var.set(directory)
        elif input_type == "image":
            file_path = filedialog.askopenfilename(
                initialdir=self.inference_input_var.get() if Path(self.inference_input_var.get()).exists() else ".",
                title="Selecionar Imagem",
                filetypes=[
                    ("Imagens", "*.jpg *.jpeg *.png *.bmp *.tiff"),
                    ("Todos os arquivos", "*.*")
                ]
            )
            if file_path:
                self.inference_input_var.set(file_path)
        elif input_type == "video":
            file_path = filedialog.askopenfilename(
                initialdir=self.inference_input_var.get() if Path(self.inference_input_var.get()).exists() else ".",
                title="Selecionar Vídeo",
                filetypes=[
                    ("Vídeos", "*.mp4 *.avi *.mov *.mkv *.flv *.wmv"),
                    ("Todos os arquivos", "*.*")
                ]
            )
            if file_path:
                self.inference_input_var.set(file_path)
    
    def update_inference_input_ui(self):
        """Atualiza UI baseado no tipo de entrada selecionado."""
        input_type = self.inference_input_type_var.get()
        
        if input_type == "directory":
            if not self.inference_input_var.get() or not Path(self.inference_input_var.get()).exists():
                self.inference_input_var.set("dataset/test")
            self.inference_browse_btn.config(text="📁")
            # Desabilitar preview para diretório
            if hasattr(self, 'preview_check'):
                self.preview_check.config(state=tk.DISABLED)
                self.show_preview_var.set(False)
        elif input_type == "image":
            if Path(self.inference_input_var.get()).is_dir():
                self.inference_input_var.set("")
            self.inference_browse_btn.config(text="🖼️")
            # Desabilitar preview para imagem
            if hasattr(self, 'preview_check'):
                self.preview_check.config(state=tk.DISABLED)
                self.show_preview_var.set(False)
        elif input_type == "video":
            if Path(self.inference_input_var.get()).is_dir():
                self.inference_input_var.set("")
            self.inference_browse_btn.config(text="📹")
            # Habilitar preview apenas para vídeo
            if hasattr(self, 'preview_check'):
                self.preview_check.config(state=tk.NORMAL)
    
    def toggle_preview_panel(self):
        """Abre/fecha a janela de preview em tempo real (sem depender do PanedWindow)."""
        # Só faz sentido para vídeo
        if self.inference_input_type_var.get() != "video":
            self.show_preview_var.set(False)
            return

        if self.show_preview_var.get():
            self._ensure_preview_window()
        else:
            self._close_preview_window()

    def _ensure_preview_window(self):
        if self.preview_window and self.preview_window.winfo_exists():
            return

        win = tk.Toplevel(self.root)
        win.title("📺 Preview em Tempo Real - Predições")
        win.configure(bg="#000000")
        # Ajustar para melhor visualização horizontal - usar mais largura
        self._maximize_window(win, fallback_geometry="1400x800", minsize=(1200, 600))

        # Se o usuário fechar a janela no “X”, desmarca o checkbox
        def on_close():
            self.show_preview_var.set(False)
            self._close_preview_window()

        win.protocol("WM_DELETE_WINDOW", on_close)

        header = tk.Frame(win, bg="#111111")
        header.pack(fill=tk.X)
        tk.Label(
            header,
            text="Preview em Tempo Real (velocidade original do vídeo)",
            bg="#111111",
            fg="#ffffff",
            font=("Helvetica", 12, "bold"),
            padx=12,
            pady=8,
        ).pack(side=tk.LEFT)

        self.preview_label = tk.Label(
            win,
            text="Aguardando frames...",
            bg="#000000",
            fg="#ffffff",
            font=("Helvetica", 12),
        )
        self.preview_label.pack(fill=tk.BOTH, expand=True)

        self.preview_window = win

    def _close_preview_window(self):
        try:
            if self.preview_window and self.preview_window.winfo_exists():
                self.preview_window.destroy()
        finally:
            self.preview_window = None
            self.preview_label = None
    
    def update_preview_frame(self, frame_image):
        """Atualiza o frame no preview."""
        if self.preview_label and self.preview_window and self.preview_window.winfo_exists():
            # Converter PIL Image para PhotoImage do Tkinter
            from PIL import Image, ImageTk
            import numpy as np
            import cv2
            
            # Se for numpy array (OpenCV), converter para PIL
            if isinstance(frame_image, np.ndarray):
                frame_image = Image.fromarray(cv2.cvtColor(frame_image, cv2.COLOR_BGR2RGB))
            
            # Redimensionar para caber no painel mantendo aspect ratio - melhorar visualização horizontal
            max_width = 1280  # Aumentar largura para melhor visualização
            max_height = 720
            
            img_width, img_height = frame_image.size
            scale = min(max_width / img_width, max_height / img_height, 1.0)
            
            if scale < 1.0:
                new_width = int(img_width * scale)
                new_height = int(img_height * scale)
                frame_image = frame_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Converter para PhotoImage
            photo = ImageTk.PhotoImage(frame_image)
            
            # Atualizar label
            self.preview_label.config(image=photo, text="")
            self.preview_label.image = photo  # Manter referência
            
            self.root.update_idletasks()

    def _maximize_window(self, window, fallback_geometry="1200x800", minsize=(900, 650)):
        """Tenta abrir a janela em tamanho máximo/cheio, com fallback para geometria grande."""
        try:
            window.minsize(minsize[0], minsize[1])
        except Exception:
            pass

        # Windows/Linux geralmente suportam 'zoomed'. No macOS pode falhar; usamos fallback.
        try:
            window.state("zoomed")
            return
        except Exception:
            pass

        try:
            sw = window.winfo_screenwidth()
            sh = window.winfo_screenheight()
            # Usar quase tela cheia (deixa margens pequenas para não “pular” em setups diferentes)
            w = max(minsize[0], int(sw * 0.95))
            h = max(minsize[1], int(sh * 0.90))
            x = max(0, int((sw - w) / 2))
            y = max(0, int((sh - h) / 3))
            window.geometry(f"{w}x{h}+{x}+{y}")
        except Exception:
            window.geometry(fallback_geometry)
    
    def update_status_bar(self, message):
        """Atualiza barra de status."""
        self.status_bar.config(text=message)
        self.root.update_idletasks()
    
    def log_message(self, text_widget, message, tag=None):
        """Adiciona mensagem ao log."""
        text_widget.insert(tk.END, message + "\n")
        text_widget.see(tk.END)
        self.root.update_idletasks()
    
    def verify_dataset(self):
        """Verifica estrutura do dataset."""
        dataset_dir = self.dataset_dest_var.get()
        
        def verify_thread():
            try:
                cmd = [
                    sys.executable,
                    "scripts/download_roboflow_coco.py",
                    "--use_existing", dataset_dir,
                    "--dataset_dir", dataset_dir
                ]
                
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1
                )
                
                for line in process.stdout:
                    self.log_message(self.download_log, line.strip())
                
                process.wait()
                
                if process.returncode == 0:
                    self.log_message(self.download_log, "\n✅ Verificação concluída!")
                    self.update_status_bar("Dataset verificado!")
                else:
                    self.log_message(self.download_log, "\n❌ Erro na verificação!")
                    self.update_status_bar("Erro na verificação")
            
            except Exception as e:
                self.log_message(self.download_log, f"\n❌ Erro: {e}")
                messagebox.showerror("Erro", f"Erro ao verificar dataset: {e}")
        
        threading.Thread(target=verify_thread, daemon=True).start()
    
    def toggle_existing_dataset(self):
        """Mostra ou esconde o frame de dataset existente."""
        if self.use_existing_var.get():
            self.existing_frame.pack(fill=tk.X, pady=(0, 20), before=self.dataset_dest_frame)
        else:
            self.existing_frame.pack_forget()
    
    def download_dataset(self):
        """Baixa ou carrega dataset usando método automático."""
        dataset_dir = self.dataset_dest_var.get()
        
        self.log_message(self.download_log, "="*70)
        
        # Se usar dataset existente
        if self.use_existing_var.get():
            # Usar dataset existente
            existing_path = self.existing_dataset_var.get()
            if not existing_path:
                messagebox.showerror("Erro", "Informe o caminho do dataset existente!")
                return
            
            self.log_message(self.download_log, f"📂 Carregando dataset existente...")
            self.log_message(self.download_log, f"   Origem: {existing_path}")
            self.log_message(self.download_log, f"   Destino: {dataset_dir}")
            self.update_status_bar("Carregando dataset existente...")
            
            def load_thread():
                try:
                    cmd = [
                        sys.executable,
                        "scripts/download_roboflow_coco.py",
                        "--use_existing", existing_path,
                        "--dataset_dir", dataset_dir
                    ]
                    
                    process = subprocess.Popen(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True,
                        bufsize=1
                    )
                    
                    for line in process.stdout:
                        self.log_message(self.download_log, line.strip())
                    
                    process.wait()
                    
                    if process.returncode == 0:
                        self.log_message(self.download_log, "\n✅ Dataset carregado com sucesso!")
                        self.update_status_bar("Dataset carregado!")
                        messagebox.showinfo("Sucesso", "Dataset carregado com sucesso!")
                    else:
                        self.log_message(self.download_log, "\n❌ Erro ao carregar dataset!")
                        self.update_status_bar("Erro ao carregar")
                        messagebox.showerror("Erro", "Erro ao carregar dataset. Verifique os logs.")
                
                except Exception as e:
                    self.log_message(self.download_log, f"\n❌ Erro: {e}")
                    messagebox.showerror("Erro", f"Erro: {e}")
            
            threading.Thread(target=load_thread, daemon=True).start()
            return
        
        # Download do Roboflow (método automático)
        version = self.version_var.get()
        download_url = self.download_url_var.get().strip()
        
        self.log_message(self.download_log, f"📥 Iniciando download automático...")
        self.log_message(self.download_log, f"   Versão: {version}")
        self.log_message(self.download_log, f"   Destino: {dataset_dir}")
        if download_url:
            self.log_message(self.download_log, f"   URL Raw fornecida: {download_url[:60]}...")
        else:
            self.log_message(self.download_log, f"   Tentando SDK primeiro (sem URL)...")
        self.update_status_bar(f"Baixando dataset versão {version}...")
        
        def download_thread():
            try:
                # Método automático: tenta SDK primeiro, se falhar usa curl
                cmd = [
                    sys.executable,
                    "scripts/download_roboflow_coco.py",
                    "--dataset_dir", dataset_dir,
                    "--version", version,
                    "--method", "auto"
                ]
                
                # Se URL fornecida, adicionar para fallback
                if download_url:
                    # Validar URL básica
                    if download_url.startswith(("http://", "https://")):
                        cmd.extend(["--download_url", download_url])
                        self.log_message(self.download_log, f"\n📥 URL Raw configurada para fallback")
                    else:
                        self.log_message(self.download_log, f"\n⚠️  URL inválida, ignorando. Tentando apenas SDK...")
                
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1
                )
                
                for line in process.stdout:
                    self.log_message(self.download_log, line.strip())
                
                process.wait()
                
                if process.returncode == 0:
                    self.log_message(self.download_log, "\n✅ Download concluído!")
                    self.update_status_bar("Download concluído!")
                    messagebox.showinfo("Sucesso", "Dataset baixado com sucesso!")
                else:
                    # Se falhou e temos URL, tentar curl diretamente
                    if download_url and download_url.startswith(("http://", "https://")):
                        self.log_message(self.download_log, "\n⚠️  SDK falhou. Tentando método curl com URL fornecida...")
                        cmd_curl = [
                            sys.executable,
                            "scripts/download_roboflow_coco.py",
                            "--dataset_dir", dataset_dir,
                            "--download_url", download_url
                        ]
                        
                        process_curl = subprocess.Popen(
                            cmd_curl,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            text=True,
                            bufsize=1
                        )
                        
                        for line in process_curl.stdout:
                            self.log_message(self.download_log, line.strip())
                        
                        process_curl.wait()
                        
                        if process_curl.returncode == 0:
                            self.log_message(self.download_log, "\n✅ Download concluído com curl!")
                            self.update_status_bar("Download concluído!")
                            messagebox.showinfo("Sucesso", "Dataset baixado com sucesso usando curl!")
                        else:
                            error_msg = "Erro ao baixar dataset. Ambos os métodos falharam."
                            self.log_message(self.download_log, f"\n❌ {error_msg}")
                            self.update_status_bar("Erro no download")
                            messagebox.showerror("Erro", f"{error_msg} Verifique os logs.")
                    else:
                        error_msg = "Erro ao baixar dataset. SDK falhou e nenhuma URL Raw fornecida."
                        self.log_message(self.download_log, f"\n❌ {error_msg}")
                        self.log_message(self.download_log, "\n💡 Dica: Cole a URL Raw do Roboflow no campo 'URL Raw (opcional)' e tente novamente.")
                        self.update_status_bar("Erro no download")
                        messagebox.showerror(
                            "Erro",
                            f"{error_msg}\n\n"
                            "Para obter a URL Raw:\n"
                            "1. No Roboflow, escolha 'Show download code'\n"
                            "2. Copie a URL direta (Raw URL)\n"
                            "3. Cole no campo 'URL Raw (opcional)'\n"
                            "4. Tente novamente"
                        )
            
            except Exception as e:
                self.log_message(self.download_log, f"\n❌ Erro: {e}")
                import traceback
                self.log_message(self.download_log, traceback.format_exc())
                messagebox.showerror("Erro", f"Erro: {e}")
        
        threading.Thread(target=download_thread, daemon=True).start()
    
    def start_training(self):
        """Inicia treinamento."""
        # Validar parâmetros básicos
        try:
            epochs = int(self.epochs_var.get())
            batch_size = int(self.batch_size_var.get())
            img_size = int(self.img_size_var.get())
            learning_rate = float(self.learning_rate_var.get())
            gradient_accum = int(self.gradient_accum_var.get())
            save_steps = int(self.save_steps_var.get())
            eval_steps = int(self.eval_steps_var.get())
            
            # Parâmetros avançados
            weight_decay = float(self.weight_decay_var.get())
            warmup_steps = int(self.warmup_steps_var.get())
            warmup_ratio_str = self.warmup_ratio_var.get().strip()
            warmup_ratio = float(warmup_ratio_str) if warmup_ratio_str else None
            lr_scheduler_type = self.lr_scheduler_var.get()
            adam_beta1 = float(self.adam_beta1_var.get())
            adam_beta2 = float(self.adam_beta2_var.get())
            adam_epsilon = float(self.adam_epsilon_var.get())
            max_grad_norm = float(self.max_grad_norm_var.get())
            fp16 = self.fp16_var.get()
        except ValueError as e:
            messagebox.showerror("Erro", f"Parâmetros inválidos: {e}")
            return
        
        # Verificar dataset completo
        dataset_dir = self.dataset_dir_var.get()
        dataset_path = Path(dataset_dir)
        
        # Verificar todos os splits necessários
        required_splits = ["train", "valid", "test"]
        missing_splits = []
        
        for split in required_splits:
            json_file = dataset_path / f"{split}/_annotations.coco.json"
            if not json_file.exists():
                missing_splits.append(split)
        
        if missing_splits:
            error_msg = f"Dataset incompleto! Splits faltando: {', '.join(missing_splits)}\n\n"
            error_msg += f"Dataset em: {dataset_dir}\n\n"
            error_msg += "Certifique-se de que:\n"
            error_msg += "1. O dataset foi baixado completamente\n"
            error_msg += "2. Todos os splits (train/valid/test) estão presentes\n"
            error_msg += "3. Use a aba 'Download Dataset' para baixar ou carregar o dataset"
            messagebox.showerror("Erro", error_msg)
            return
        
        # Verificar se há imagens e anotações
        try:
            import json
            train_json = dataset_path / "train/_annotations.coco.json"
            with open(train_json, 'r') as f:
                train_data = json.load(f)
            
            n_images = len(train_data.get("images", []))
            n_annotations = len(train_data.get("annotations", []))
            
            if n_images == 0:
                messagebox.showerror("Erro", "Dataset vazio! Não há imagens no split de treinamento.")
                return
            
            if n_annotations == 0:
                messagebox.showerror("Erro", "Dataset sem anotações! Não há anotações no split de treinamento.")
                return
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao verificar dataset: {e}")
            return
        
        # Desabilitar botão
        self.train_btn.config(state=tk.DISABLED)
        self.stop_train_btn.config(state=tk.NORMAL)
        
        self.log_message(self.training_log, "="*70)
        self.log_message(self.training_log, "Iniciando treinamento...")
        self.log_message(self.training_log, f"Épocas: {epochs}")
        self.log_message(self.training_log, f"Batch Size: {batch_size}")
        self.log_message(self.training_log, f"Tamanho da Imagem: {img_size}")
        self.log_message(self.training_log, f"Learning Rate: {learning_rate}")
        self.log_message(self.training_log, "="*70)
        
        def training_thread():
            try:
                cmd = [
                    sys.executable, "src/train_rtdetr.py",
                    "--dataset_dir", dataset_dir,
                    "--out_dir", self.output_dir_var.get(),
                    "--epochs", str(epochs),
                    "--batch_size", str(batch_size),
                    "--img_size", str(img_size),
                    "--learning_rate", str(learning_rate),
                    "--gradient_accumulation_steps", str(gradient_accum),
                    "--save_steps", str(save_steps),
                    "--eval_steps", str(eval_steps),
                    "--weight_decay", str(weight_decay),
                    "--warmup_steps", str(warmup_steps),
                    "--lr_scheduler_type", lr_scheduler_type,
                    "--adam_beta1", str(adam_beta1),
                    "--adam_beta2", str(adam_beta2),
                    "--adam_epsilon", str(adam_epsilon),
                    "--max_grad_norm", str(max_grad_norm),
                ]
                
                # Adicionar warmup_ratio se fornecido
                if warmup_ratio is not None:
                    cmd.extend(["--warmup_ratio", str(warmup_ratio)])
                
                # Adicionar fp16 se habilitado
                if fp16:
                    cmd.append("--fp16")
                
                self.training_process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1
                )
                
                for line in self.training_process.stdout:
                    self.log_message(self.training_log, line.strip())
                
                self.training_process.wait()
                
                if self.training_process.returncode == 0:
                    self.log_message(self.training_log, "\n✅ Treinamento concluído!")
                    self.update_status_bar("Treinamento concluído!")
                    messagebox.showinfo("Sucesso", "Treinamento concluído com sucesso!")
                else:
                    self.log_message(self.training_log, "\n❌ Erro no treinamento!")
                    self.update_status_bar("Erro no treinamento")
            
            except Exception as e:
                self.log_message(self.training_log, f"\n❌ Erro: {e}")
                messagebox.showerror("Erro", f"Erro: {e}")
            finally:
                self.train_btn.config(state=tk.NORMAL)
                self.stop_train_btn.config(state=tk.DISABLED)
                self.training_process = None
        
        threading.Thread(target=training_thread, daemon=True).start()
    
    def stop_training(self):
        """Para treinamento."""
        if self.training_process:
            self.training_process.terminate()
            self.log_message(self.training_log, "\n⚠️ Treinamento interrompido pelo usuário")
            self.update_status_bar("Treinamento interrompido")
    
    def start_inference(self):
        """Inicia inferência."""
        model_dir = f"runs_rtdetr/{self.model_choice_var.get()}"
        if not Path(model_dir).exists():
            messagebox.showerror("Erro", f"Modelo não encontrado: {model_dir}")
            return
        
        input_path = self.inference_input_var.get()
        input_type = self.inference_input_type_var.get()
        
        # Validar entrada baseado no tipo
        if input_type == "directory":
            if not Path(input_path).exists():
                messagebox.showerror("Erro", f"Diretório não encontrado: {input_path}")
                return
        else:  # image ou video
            if not Path(input_path).exists():
                messagebox.showerror("Erro", f"Arquivo não encontrado: {input_path}")
                return
        
        score_threshold = self.score_threshold_var.get()
        iou_threshold = self.iou_threshold_var.get()

        # Para vídeo: abrir preview automaticamente (sem precisar marcar checkbox)
        if input_type == "video":
            if not self.show_preview_var.get():
                self.show_preview_var.set(True)
            self._ensure_preview_window()
        
        self.inference_btn.config(state=tk.DISABLED)
        self.stop_inference_btn.config(state=tk.NORMAL)
        
        self.log_message(self.inference_log, "="*70)
        self.log_message(self.inference_log, "Iniciando predição...")
        self.log_message(self.inference_log, f"Modelo: {model_dir}")
        self.log_message(self.inference_log, f"Tipo: {input_type}")
        self.log_message(self.inference_log, f"Input: {input_path}")
        self.log_message(self.inference_log, f"Score Threshold: {score_threshold:.2f}")
        self.log_message(self.inference_log, f"IOU Threshold: {iou_threshold:.2f}")
        self.log_message(self.inference_log, "="*70)
        
        def inference_thread():
            try:
                # Se preview está ativo e é vídeo, processar diretamente (e atualizar janela)
                if input_type == "video" and self.show_preview_var.get():
                    self._process_video_with_preview(
                        model_dir, input_path, score_threshold, iou_threshold
                    )
                    return
                
                # Determinar qual script usar
                if input_type == "video":
                    # Criar diretório de saída se não existir
                    output_dir = Path(self.inference_output_var.get())
                    output_dir.mkdir(parents=True, exist_ok=True)
                    
                    # Usar script de vídeo
                    out_video_path = output_dir / f"annotated_{Path(input_path).name}"
                    cmd = [
                        sys.executable, "src/infer_video.py",
                        "--model_dir", model_dir,
                        "--video_path", input_path,
                        "--out_path", str(out_video_path),
                        "--score_threshold", str(score_threshold),
                        "--dataset_dir", "dataset"
                    ]
                    
                    # Adicionar preview se solicitado
                    if self.show_preview_var.get():
                        cmd.append("--show_preview")
                else:
                    # Usar script de imagens (suporta diretório ou arquivo único)
                    cmd = [
                        sys.executable, "src/infer_images.py",
                        "--model_dir", model_dir,
                        "--out_dir", self.inference_output_var.get(),
                        "--score_threshold", str(score_threshold),
                        "--iou_threshold", str(iou_threshold),
                        "--dataset_dir", "dataset"
                    ]
                    
                    if input_type == "image":
                        cmd.extend(["--input_file", input_path])
                    else:  # directory
                        cmd.extend(["--input_dir", input_path])
                
                self.inference_process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1
                )
                
                for line in self.inference_process.stdout:
                    self.log_message(self.inference_log, line.strip())
                
                self.inference_process.wait()
                
                if self.inference_process.returncode == 0:
                    self.log_message(self.inference_log, "\n✅ Predição concluída!")
                    self.update_status_bar("Predição concluída!")
                    messagebox.showinfo("Sucesso", f"Predição concluída! Resultados em: {self.inference_output_var.get()}")
                else:
                    self.log_message(self.inference_log, "\n❌ Erro na predição!")
                    self.update_status_bar("Erro na predição")
            
            except Exception as e:
                self.log_message(self.inference_log, f"\n❌ Erro: {e}")
                messagebox.showerror("Erro", f"Erro: {e}")
            finally:
                self.inference_btn.config(state=tk.NORMAL)
                self.stop_inference_btn.config(state=tk.DISABLED)
                self.inference_process = None
        
        threading.Thread(target=inference_thread, daemon=True).start()
    
    def _process_video_with_preview(self, model_dir, video_path, score_threshold, iou_threshold):
        """Processa vídeo diretamente com preview em tempo real E salva o vídeo."""
        try:
            import cv2
            import torch
            from PIL import Image
            import numpy as np
            sys.path.insert(0, str(Path(__file__).parent / "src"))
            from transformers import AutoImageProcessor, AutoModelForObjectDetection
            from coco_utils import load_coco_json
            
            self.log_message(self.inference_log, "📺 Modo preview ativo - processando em tempo real...")
            
            # Criar diretório de saída se não existir
            output_dir = Path(self.inference_output_var.get())
            output_dir.mkdir(parents=True, exist_ok=True)
            out_video_path = output_dir / f"annotated_{Path(video_path).name}"
            
            self.log_message(self.inference_log, f"💾 Vídeo será salvo em: {out_video_path}")
            
            # Carregar modelo
            device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
            model = AutoModelForObjectDetection.from_pretrained(model_dir)
            model.to(device)
            model.eval()
            
            processor = AutoImageProcessor.from_pretrained(model_dir)
            
            # Carregar categorias
            category_names = {}
            dataset_dir = Path("dataset")
            for split in ["train", "valid", "test"]:
                json_path = dataset_dir / f"{split}/_annotations.coco.json"
                if json_path.exists():
                    coco_data = load_coco_json(json_path)
                    category_names = {cat["id"]: cat["name"] for cat in coco_data["categories"]}
                    break
            
            # Abrir vídeo
            cap = cv2.VideoCapture(str(video_path))
            if not cap.isOpened():
                raise RuntimeError(f"Não foi possível abrir o vídeo: {video_path}")
            
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            self.log_message(self.inference_log, f"📊 FPS: {fps}, Resolução: {width}x{height}, Frames: {total_frames}")
            
            # Criar VideoWriter para salvar o vídeo processado
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out_video = cv2.VideoWriter(str(out_video_path), fourcc, fps, (width, height))
            
            if not out_video.isOpened():
                raise RuntimeError(f"Não foi possível criar vídeo de saída: {out_video_path}")
            
            self.log_message(self.inference_log, f"💾 Salvando vídeo processado em: {out_video_path}")
            
            frame_count = 0
            frame_time = 1.0 / fps if fps > 0 else 0.033  # Tempo por frame em segundos
            next_frame_ts = time.perf_counter()
            
            with torch.no_grad():
                while True:
                    # Se o usuário desmarcou o preview ou fechou a janela, parar suavemente
                    if not self.show_preview_var.get():
                        break
                    if not (self.preview_window and self.preview_window.winfo_exists()):
                        break
                    
                    ret, frame = cap.read()
                    if not ret:
                        break
                    
                    frame_count += 1
                    
                    # Converter para PIL
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    pil_image = Image.fromarray(frame_rgb)
                    
                    # Processar
                    inputs = processor(images=pil_image, return_tensors="pt")
                    inputs = {k: v.to(device) for k, v in inputs.items()}
                    
                    # Predição
                    outputs = model(**inputs)
                    target_sizes = torch.tensor([pil_image.size[::-1]]).to(device)
                    results = processor.post_process_object_detection(
                        outputs, target_sizes=target_sizes, threshold=score_threshold
                    )[0]
                    
                    # Coletar detecções e identificar a melhor (maior score)
                    det_boxes = results["boxes"].cpu().numpy()
                    det_scores = results["scores"].cpu().numpy()
                    det_labels = results["labels"].cpu().numpy()

                    best_idx = None
                    best_score = -1.0
                    for i, s in enumerate(det_scores):
                        fs = float(s)
                        if fs > best_score:
                            best_score = fs
                            best_idx = i

                    # Desenhar detecções (marcar a melhor com centróide vermelho)
                    for i, (box, score, label) in enumerate(
                        zip(det_boxes, det_scores, det_labels)
                    ):
                        x1, y1, x2, y2 = [int(c) for c in box.tolist()]
                        label_name = category_names.get(int(label), f"Class_{int(label)}")

                        # BBox padrão (verde)
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(
                            frame,
                            f"{label_name} {float(score):.2f}",
                            (x1, max(0, y1 - 10)),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.6,
                            (0, 255, 0),
                            2,
                        )

                        # Melhor bbox: desenhar centróide (círculo vermelho pequeno)
                        if best_idx is not None and i == best_idx:
                            cx = int((x1 + x2) / 2)
                            cy = int((y1 + y2) / 2)
                            cv2.circle(frame, (cx, cy), 6, (0, 0, 255), -1)  # vermelho (BGR)
                            cv2.circle(frame, (cx, cy), 6, (255, 255, 255), 2)  # borda branca
                    
                    # Salvar frame no vídeo de saída
                    out_video.write(frame)
                    
                    # Atualizar preview em tempo real
                    self.update_preview_frame(frame)
                    
                    # Log progresso a cada 30 frames
                    if frame_count % 30 == 0:
                        progress = (frame_count / total_frames) * 100
                        self.log_message(self.inference_log, f"Processando... {frame_count}/{total_frames} frames ({progress:.1f}%)")
                    
                    # Manter velocidade natural do vídeo (com compensação de tempo de processamento)
                    next_frame_ts += frame_time
                    sleep_s = next_frame_ts - time.perf_counter()
                    if sleep_s > 0:
                        time.sleep(sleep_s)
            
            # Fechar recursos
            cap.release()
            out_video.release()
            
            self.log_message(self.inference_log, f"\n✅ Preview concluído! {frame_count} frames processados")
            self.log_message(self.inference_log, f"💾 Vídeo salvo em: {out_video_path}")
            self.update_status_bar("Preview concluído! Vídeo salvo.")
            
            # Mostrar mensagem de sucesso
            messagebox.showinfo("Sucesso", f"Vídeo processado e salvo!\n\nLocalização: {out_video_path}")
            
        except Exception as e:
            self.log_message(self.inference_log, f"\n❌ Erro no preview: {e}")
            import traceback
            self.log_message(self.inference_log, traceback.format_exc())
    
    def stop_inference(self):
        """Para inferência."""
        if self.inference_process:
            self.inference_process.terminate()
            self.inference_process = None
        self.log_message(self.inference_log, "\n⚠️ Predição interrompida pelo usuário")
        self.update_status_bar("Predição interrompida")
        # Fechar janela de preview se estiver aberta
        self.show_preview_var.set(False)
        self._close_preview_window()
    
    def start_evaluation(self):
        """Inicia avaliação."""
        model_dir = f"runs_rtdetr/{self.eval_model_var.get()}"
        if not Path(model_dir).exists():
            messagebox.showerror("Erro", f"Modelo não encontrado: {model_dir}")
            return
        
        split = self.eval_split_var.get()
        
        self.log_message(self.eval_log, "="*70)
        self.log_message(self.eval_log, f"Avaliando modelo {model_dir} no split {split}...")
        self.log_message(self.eval_log, "="*70)
        
        def eval_thread():
            try:
                cmd = [
                    sys.executable, "src/eval_coco.py",
                    "--model_dir", model_dir,
                    "--dataset_dir", "dataset",
                    "--split", split
                ]
                
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1
                )
                
                for line in process.stdout:
                    self.log_message(self.eval_log, line.strip())
                
                process.wait()
                
                if process.returncode == 0:
                    self.log_message(self.eval_log, "\n✅ Avaliação concluída!")
                    self.update_status_bar("Avaliação concluída!")
                else:
                    self.log_message(self.eval_log, "\n❌ Erro na avaliação!")
            
            except Exception as e:
                self.log_message(self.eval_log, f"\n❌ Erro: {e}")
                messagebox.showerror("Erro", f"Erro: {e}")
        
        threading.Thread(target=eval_thread, daemon=True).start()
    
    def check_initial_status(self):
        """Verifica status inicial."""
        self.update_status()
    
    def update_status(self):
        """Atualiza status do sistema."""
        self.status_text.delete(1.0, tk.END)
        
        status_lines = []
        status_lines.append("="*70)
        status_lines.append("STATUS DO SISTEMA")
        status_lines.append("="*70)
        status_lines.append("")
        
        # Verificar dataset
        status_lines.append("📊 DATASET:")
        for split in ["train", "valid", "test"]:
            json_path = Path(f"dataset/{split}/_annotations.coco.json")
            if json_path.exists():
                try:
                    with open(json_path) as f:
                        data = json.load(f)
                    status_lines.append(f"  ✅ {split}: {len(data.get('images', []))} imagens, {len(data.get('annotations', []))} anotações")
                except:
                    status_lines.append(f"  ⚠️  {split}: Arquivo existe mas não pode ser lido")
            else:
                status_lines.append(f"  ❌ {split}: Não encontrado")
        
        status_lines.append("")
        
        # Verificar modelos
        status_lines.append("🤖 MODELOS:")
        model_best = Path("runs_rtdetr/model_best")
        model_final = Path("runs_rtdetr/model_final")
        
        if model_best.exists():
            status_lines.append("  ✅ model_best: Disponível")
        else:
            status_lines.append("  ❌ model_best: Não encontrado")
        
        if model_final.exists():
            status_lines.append("  ✅ model_final: Disponível")
        else:
            status_lines.append("  ❌ model_final: Não encontrado")
        
        status_lines.append("")
        
        # Verificar dependências
        status_lines.append("🐍 DEPENDÊNCIAS:")
        try:
            import torch
            status_lines.append(f"  ✅ PyTorch: {torch.__version__}")
            status_lines.append(f"  ✅ MPS: {torch.backends.mps.is_available()}")
        except ImportError:
            status_lines.append("  ❌ PyTorch: Não instalado")
        
        try:
            import transformers
            status_lines.append(f"  ✅ Transformers: {transformers.__version__}")
        except ImportError:
            status_lines.append("  ❌ Transformers: Não instalado")
        
        status_lines.append("")
        status_lines.append("="*70)
        
        self.status_text.insert(1.0, "\n".join(status_lines))


def main():
    """Função principal."""
    root = tk.Tk()
    app = ModernTkinterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

