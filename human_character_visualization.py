import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Polygon, FancyBboxPatch, Arc, Wedge
from matplotlib.path import Path
import matplotlib.patches as mpatches
import numpy as np
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.gridspec import GridSpec

class CharacterVisualizationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Character Trait Visualization")
        self.root.geometry("1400x900")
        
        # Define traits and their corresponding shapes with descriptions
        self.trait_info = {
            'compassionate': {
                'shape': 'circle',
                'color': 'blue',
                'description': 'Caring deeply about others\' well-being',
                'rationale': 'Circle: Universal symbol of wholeness and inclusion (Jung, 1964)'
            },
            'strong_willed': {
                'shape': 'square',
                'color': 'green',
                'description': 'Determined and persistent in goals',
                'rationale': 'Square: Stability and firmness in Gestalt psychology'
            },
            'creative': {
                'shape': 'spiral',
                'color': 'orange',
                'description': 'Imaginative and original thinking',
                'rationale': 'Spiral: Growth and evolution patterns (Fibonacci in nature)'
            },
            'analytical': {
                'shape': 'triangle',
                'color': 'red',
                'description': 'Logical and systematic approach',
                'rationale': 'Triangle: Directional focus and structural thinking'
            },
            'adaptable': {
                'shape': 'hexagon',
                'color': 'purple',
                'description': 'Flexible and open to change',
                'rationale': 'Hexagon: Efficient natural form allowing multiple connections'
            },
            'empathetic': {
                'shape': 'heart',
                'color': 'pink',
                'description': 'Understanding others\' emotions',
                'rationale': 'Heart: Cross-cultural symbol of emotional connection'
            },
            'ambitious': {
                'shape': 'arrow',
                'color': 'darkgreen',
                'description': 'Driven to achieve success',
                'rationale': 'Arrow: Upward movement and goal direction'
            },
            'peaceful': {
                'shape': 'oval',
                'color': 'lightblue',
                'description': 'Calm and harmonious nature',
                'rationale': 'Oval: Smooth curves reduce visual tension (Arnheim, 1974)'
            },
            'organized': {
                'shape': 'grid',
                'color': 'brown',
                'description': 'Structured and methodical',
                'rationale': 'Grid: Order and systematic arrangement'
            },
            'intuitive': {
                'shape': 'crescent',
                'color': 'indigo',
                'description': 'Trusting inner wisdom',
                'rationale': 'Crescent: Symbol of inner knowing across cultures'
            },
            'confident': {
                'shape': 'star',
                'color': 'gold',
                'description': 'Self-assured and positive',
                'rationale': 'Star: Radiating energy and prominence'
            },
            'patient': {
                'shape': 'line',
                'color': 'gray',
                'description': 'Calm endurance and tolerance',
                'rationale': 'Line: Steady, unchanging continuity'
            },
            'curious': {
                'shape': 'question',
                'color': 'magenta',
                'description': 'Eager to learn and explore',
                'rationale': 'Question mark: Literal representation of inquiry'
            },
            'loyal': {
                'shape': 'diamond',
                'color': 'cyan',
                'description': 'Faithful and devoted',
                'rationale': 'Diamond: Durability and preciousness'
            },
            'optimistic': {
                'shape': 'sun',
                'color': 'yellow',
                'description': 'Positive outlook on life',
                'rationale': 'Sun: Universal symbol of positivity and warmth'
            },
            'decisive': {
                'shape': 'pentagon',
                'color': 'maroon',
                'description': 'Quick and firm in decisions',
                'rationale': 'Pentagon: Strong, definitive shape with clear angles'
            },
            'humble': {
                'shape': 'small_circle',
                'color': 'lightgray',
                'description': 'Modest and unpretentious',
                'rationale': 'Small circle: Minimized presence, simplicity'
            },
            'courageous': {
                'shape': 'shield',
                'color': 'darkblue',
                'description': 'Brave in facing challenges',
                'rationale': 'Shield: Protection and forward-facing strength'
            },
            'wise': {
                'shape': 'eye',
                'color': 'darkgray',
                'description': 'Deep understanding and insight',
                'rationale': 'Eye: Vision and perception across wisdom traditions'
            },
            'playful': {
                'shape': 'wave',
                'color': 'teal',
                'description': 'Fun-loving and lighthearted',
                'rationale': 'Wave: Dynamic movement and flow'
            }
        }
        
        # Questions for the survey
        self.questions = [
            ("I often feel deeply moved by others' experiences", 'compassionate'),
            ("I go out of my way to help those in need", 'compassionate'),
            ("I stick to my decisions even when faced with opposition", 'strong_willed'),
            ("I rarely give up on my goals", 'strong_willed'),
            ("I enjoy finding new ways to solve problems", 'creative'),
            ("I often come up with original ideas", 'creative'),
            ("I prefer to analyze situations before making decisions", 'analytical'),
            ("I enjoy breaking down complex problems", 'analytical'),
            ("I easily adjust to new situations", 'adaptable'),
            ("Change doesn't bother me much", 'adaptable'),
            ("I can sense others' emotions easily", 'empathetic'),
            ("I understand how others feel", 'empathetic'),
            ("I set high goals for myself", 'ambitious'),
            ("I'm driven to achieve success", 'ambitious'),
            ("I prefer harmony over conflict", 'peaceful'),
            ("I stay calm in stressful situations", 'peaceful'),
            ("I like having everything in its place", 'organized'),
            ("I plan my tasks carefully", 'organized'),
            ("I trust my gut feelings", 'intuitive'),
            ("I often know things without being told", 'intuitive'),
        ]
        
        self.current_question = 0
        self.responses = {trait: 0 for trait in self.trait_info}
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Title
        self.title_label = ttk.Label(self.main_frame, text="Character Trait Assessment", 
                                    font=('Arial', 16, 'bold'))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=20)
        
        # Progress bar
        self.progress = ttk.Progressbar(self.main_frame, length=400, mode='determinate')
        self.progress.grid(row=1, column=0, columnspan=2, pady=10)
        
        # Question label
        self.question_label = ttk.Label(self.main_frame, text="", font=('Arial', 12),
                                       wraplength=500)
        self.question_label.grid(row=2, column=0, columnspan=2, pady=20)
        
        # Response scale
        self.scale_frame = ttk.Frame(self.main_frame)
        self.scale_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        self.response_var = tk.IntVar(value=3)
        
        # Scale labels
        labels = ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]
        for i, label in enumerate(labels, 1):
            ttk.Radiobutton(self.scale_frame, text=label, variable=self.response_var, 
                           value=i).grid(row=0, column=i-1, padx=10)
        
        # Next button
        self.next_button = ttk.Button(self.main_frame, text="Next", command=self.next_question)
        self.next_button.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Start the survey
        self.show_question()
        
    def show_question(self):
        if self.current_question < len(self.questions):
            question_text, _ = self.questions[self.current_question]
            self.question_label.config(text=f"Question {self.current_question + 1}: {question_text}")
            self.progress['value'] = (self.current_question / len(self.questions)) * 100
            self.response_var.set(3)  # Reset to neutral
        
    def next_question(self):
        if self.current_question < len(self.questions):
            # Record response
            _, trait = self.questions[self.current_question]
            self.responses[trait] += self.response_var.get()
            
            self.current_question += 1
            
            if self.current_question < len(self.questions):
                self.show_question()
            else:
                self.show_results()
    
    def show_results(self):
        # Clear the window
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Create notebook for tabs
        notebook = ttk.Notebook(self.main_frame)
        notebook.pack(fill='both', expand=True)
        
        # Tab 1: Visualization
        viz_frame = ttk.Frame(notebook)
        notebook.add(viz_frame, text="Your Character Visualization")
        
        # Tab 2: Legend
        legend_frame = ttk.Frame(notebook)
        notebook.add(legend_frame, text="Shape Meanings")
        
        # Tab 3: Profile Analysis
        analysis_frame = ttk.Frame(notebook)
        notebook.add(analysis_frame, text="Profile Analysis")
        
        # Create the visualization
        self.create_visualization_tab(viz_frame)
        
        # Create the legend
        self.create_legend_tab(legend_frame)
        
        # Create the analysis
        self.create_analysis_tab(analysis_frame)
    
    def create_visualization_tab(self, parent):
        # Title
        title_label = ttk.Label(parent, text="Your Unique Character Profile", 
                               font=('Arial', 14, 'bold'))
        title_label.pack(pady=10)
        
        # Create the visualization
        fig = self.create_visualization()
        
        # Embed the plot in tkinter
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Button frame
        button_frame = ttk.Frame(parent)
        button_frame.pack(pady=10)
        
        # Save button
        save_button = ttk.Button(button_frame, text="Save Image", 
                               command=lambda: self.save_visualization(fig))
        save_button.pack(side=tk.LEFT, padx=5)
        
        # Restart button
        restart_button = ttk.Button(button_frame, text="Start Over", 
                                  command=self.restart)
        restart_button.pack(side=tk.LEFT, padx=5)
    
    def create_legend_tab(self, parent):
        # Create scrollable frame
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Title
        title_label = ttk.Label(scrollable_frame, text="Shape-Trait Mapping Guide", 
                               font=('Arial', 14, 'bold'))
        title_label.pack(pady=10)
        
        # Scientific explanation
        explanation_frame = ttk.Frame(scrollable_frame)
        explanation_frame.pack(fill='x', padx=20, pady=10)
        
        explanation_text = ("Shape-trait mappings are based on research in visual perception, "
                          "symbolic psychology (Jung, 1964), and Gestalt principles (Arnheim, 1974). "
                          "Each geometric form carries inherent psychological associations that "
                          "align with specific character traits.")
        
        explanation_label = ttk.Label(explanation_frame, text=explanation_text, 
                                    wraplength=700, font=('Arial', 10))
        explanation_label.pack()
        
        # Create legend figure
        fig = plt.figure(figsize=(14, 14))  # Increased height for better spacing
        gs = GridSpec(5, 4, figure=fig, hspace=0.7, wspace=0.4)  # Increased hspace
        
        # Draw each shape with its meaning
        for i, (trait, info) in enumerate(self.trait_info.items()):
            row = i // 4
            col = i % 4
            ax = fig.add_subplot(gs[row, col])
            ax.set_xlim(-2, 2)
            ax.set_ylim(-3, 2.5)  # Extended lower limit for text
            ax.axis('off')
            
            # Draw the shape
            self.draw_shape(ax, info['shape'], 0, 0.5, 0.8, info['color'])  # Moved shape up
            
            # Add label with more spacing
            trait_name = trait.replace('_', ' ').title()
            ax.text(0, -1.2, trait_name, ha='center', fontsize=11, fontweight='bold')
            ax.text(0, -1.6, info['description'], ha='center', fontsize=9, 
                   wrap=True, style='italic')
            # Add rationale
            if 'rationale' in info:
                ax.text(0, -2.2, info['rationale'], ha='center', fontsize=7,
                       wrap=True, color='gray')
        
        # Embed in tkinter
        canvas_legend = FigureCanvasTkAgg(fig, master=scrollable_frame)
        canvas_legend.draw()
        canvas_legend.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_analysis_tab(self, parent):
        # Create scrollable text widget
        text_frame = ttk.Frame(parent)
        text_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(text_frame, text="Your Character Profile Analysis", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Analysis text with enhanced formatting
        analysis_text = tk.Text(text_frame, wrap=tk.WORD, width=90, height=30,
                               font=('Arial', 11), padx=20, pady=15,
                               bg='#FAFAFA', relief=tk.FLAT, borderwidth=1)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=analysis_text.yview)
        analysis_text.configure(yscrollcommand=scrollbar.set)
        
        analysis_text.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        
        # Configure text tags for formatting
        analysis_text.tag_configure('title', font=('Arial', 20, 'bold'), foreground='#2C3E50', 
                                   spacing1=10, spacing3=10, justify='center')
        analysis_text.tag_configure('section', font=('Arial', 14, 'bold'), foreground='#2C3E50',
                                   spacing1=20, spacing3=8, underline=True)
        analysis_text.tag_configure('subsection', font=('Arial', 12, 'bold'), foreground='#34495E',
                                   spacing1=10, spacing3=5)
        analysis_text.tag_configure('body', font=('Arial', 11), spacing1=3, spacing3=3, lmargin2=20)
        analysis_text.tag_configure('highlight', font=('Arial', 11, 'bold'), foreground='#E74C3C')
        analysis_text.tag_configure('trait_name', font=('Arial', 13, 'bold'), foreground='#3498DB')
        analysis_text.tag_configure('reference', font=('Arial', 10, 'italic'), foreground='#7F8C8D')
        analysis_text.tag_configure('separator', font=('Arial', 8), foreground='#BDC3C7',
                                   justify='center', spacing1=5, spacing3=5)
        analysis_text.tag_configure('bullet', font=('Arial', 11), lmargin1=40, lmargin2=60)
        analysis_text.tag_configure('box_header', font=('Arial', 12, 'bold'), background='#E8F4F8',
                                   foreground='#2C3E50', spacing1=5, spacing3=5, 
                                   lmargin1=10, rmargin=10)
        analysis_text.tag_configure('box_content', background='#F5FAFE', lmargin1=15, 
                                   lmargin2=20, rmargin=15, spacing1=3, spacing3=3)
        
        # Generate and insert formatted analysis
        self.insert_formatted_analysis(analysis_text)
        
        analysis_text.config(state='disabled')  # Make read-only
    
    def insert_formatted_analysis(self, text_widget):
        # Calculate normalized scores
        max_score = 10
        normalized_scores = {trait: score/max_score for trait, score in self.responses.items()}
        
        # Sort traits by score
        sorted_traits = sorted(normalized_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Categorize traits
        dominant_traits = [(t, s) for t, s in sorted_traits if s >= 0.7]
        strong_traits = [(t, s) for t, s in sorted_traits if 0.5 <= s < 0.7]
        moderate_traits = [(t, s) for t, s in sorted_traits if 0.3 <= s < 0.5]
        
        # Title
        text_widget.insert('end', 'CHARACTER PROFILE ANALYSIS\n', 'title')
        text_widget.insert('end', '━' * 80 + '\n\n', 'separator')
        
        # Scientific Foundation
        text_widget.insert('end', '📚 SCIENTIFIC FOUNDATION\n', 'section')
        text_widget.insert('end', 'This assessment is grounded in established psychological research:\n\n', 'body')
        
        text_widget.insert('end', '▸ Integrated Research Frameworks:\n', 'subsection')
        frameworks = [
            ('The Big Five personality model', 'Costa & McCrae, 1992'),
            ('VIA Character Strengths framework', 'Peterson & Seligman, 2004'),
            ('Emotional Intelligence research', 'Goleman, 1995; Salovey & Mayer, 1990'),
            ('Self-Determination Theory', 'Deci & Ryan, 2000')
        ]
        for framework, citation in frameworks:
            text_widget.insert('end', f'   • {framework} ', 'body')
            text_widget.insert('end', f'({citation})\n', 'reference')
        
        text_widget.insert('end', '\n▸ Trait Categories:\n', 'subsection')
        categories = [
            ('Cognitive traits', 'analytical, creative, wise - linked to intelligence research'),
            ('Emotional traits', 'empathetic, compassionate - from emotional intelligence studies'),
            ('Volitional traits', 'strong-willed, decisive - from motivation psychology'),
            ('Social traits', 'loyal, humble - from interpersonal psychology research')
        ]
        for category, description in categories:
            text_widget.insert('end', f'   • {category}: ', 'highlight')
            text_widget.insert('end', f'{description}\n', 'body')
        
        text_widget.insert('end', '\n' + '─' * 80 + '\n\n', 'separator')
        
        # Profile Overview
        text_widget.insert('end', '👤 YOUR PROFILE OVERVIEW\n', 'section')
        text_widget.insert('end', 'Your character profile reveals a unique combination of:\n\n', 'body')
        
        # Create visual boxes for trait counts
        text_widget.insert('end', f'   ⭐ {len(dominant_traits)} ', 'highlight')
        text_widget.insert('end', 'DOMINANT TRAITS ', 'subsection')
        text_widget.insert('end', '(70-100% strength)\n', 'body')
        text_widget.insert('end', '      Your core identity traits that define your primary characteristics\n\n', 'body')
        
        text_widget.insert('end', f'   💪 {len(strong_traits)} ', 'highlight')
        text_widget.insert('end', 'STRONG TRAITS ', 'subsection')
        text_widget.insert('end', '(50-69% strength)\n', 'body')
        text_widget.insert('end', '      Important secondary traits that significantly influence your behavior\n\n', 'body')
        
        text_widget.insert('end', f'   ✓ {len(moderate_traits)} ', 'highlight')
        text_widget.insert('end', 'MODERATE TRAITS ', 'subsection')
        text_widget.insert('end', '(30-49% strength)\n', 'body')
        text_widget.insert('end', '      Supporting traits that add nuance to your personality\n', 'body')
        
        text_widget.insert('end', '\n' + '─' * 80 + '\n\n', 'separator')
        
        # Dominant Traits
        if dominant_traits:
            text_widget.insert('end', '⭐ DOMINANT TRAITS (Core Identity)\n', 'section')
            text_widget.insert('end', 'These shapes appear largest in your visualization:\n\n', 'body')
            
            for trait, score in dominant_traits:
                trait_name = trait.replace('_', ' ').title()
                shape = self.trait_info[trait]['shape'].title()
                color = self.trait_info[trait]['color']
                
                # Create visual box for each trait
                text_widget.insert('end', f'\n◆ {trait_name} ', 'trait_name')
                text_widget.insert('end', f'— {score*100:.0f}% Strength\n', 'highlight')
                
                # Trait details in a box
                text_widget.insert('end', f'Shape: {shape} | Color: {color.title()}\n', 'box_header')
                text_widget.insert('end', f'Definition: {self.trait_info[trait]["description"]}\n', 'box_content')
                text_widget.insert('end', 'Impact: This trait strongly defines how you interact with the world.\n', 'box_content')
                text_widget.insert('end', '\n', 'body')
        
        # Strong Traits
        if strong_traits:
            text_widget.insert('end', '\n' + '─' * 80 + '\n\n', 'separator')
            text_widget.insert('end', '💪 STRONG TRAITS (Important Characteristics)\n', 'section')
            text_widget.insert('end', 'These medium-sized shapes represent significant aspects:\n\n', 'body')
            
            for trait, score in strong_traits:
                trait_name = trait.replace('_', ' ').title()
                shape = self.trait_info[trait]['shape'].title()
                
                text_widget.insert('end', f'◇ {trait_name} ', 'trait_name')
                text_widget.insert('end', f'({score*100:.0f}% strength) - {shape}\n', 'body')
                text_widget.insert('end', f'   {self.trait_info[trait]["description"]}\n\n', 'body')
        
        text_widget.insert('end', '\n' + '─' * 80 + '\n\n', 'separator')
        
        # Visualization Interpretation
        text_widget.insert('end', '🎨 VISUALIZATION INTERPRETATION\n', 'section')
        text_widget.insert('end', 'Understanding your geometric profile:\n\n', 'body')
        
        interpretations = [
            ('SIZE', 'Larger shapes indicate stronger traits (Gestalt visual hierarchy)'),
            ('OPACITY', 'More solid shapes represent more dominant characteristics'),
            ('COLOR', 'Each color chosen based on color psychology research (Elliot & Maier, 2014)'),
            ('POSITION', 'Shapes arranged in a modified Fibonacci spiral pattern')
        ]
        for aspect, explanation in interpretations:
            text_widget.insert('end', f'▸ {aspect}: ', 'subsection')
            text_widget.insert('end', f'{explanation}\n', 'body')
        
        text_widget.insert('end', '\n' + '─' * 80 + '\n\n', 'separator')
        
        # Spatial Arrangement
        text_widget.insert('end', '🌀 SPATIAL ARRANGEMENT LOGIC\n', 'section')
        text_widget.insert('end', 'The positioning follows visual perception principles:\n\n', 'body')
        
        spatial_points = [
            ('Fibonacci Spiral', 'Based on the golden ratio found throughout nature'),
            ('Hierarchical Center', 'Strongest traits closer to center (attention theory)'),
            ('72° Distribution', 'Shapes spread evenly to avoid visual clustering'),
            ('Progressive Radius', 'Each trait placed 0.5 units further from center'),
            ('Personality Mandala', 'Creates a balanced, holistic representation')
        ]
        for point, explanation in spatial_points:
            text_widget.insert('end', f'◆ {point}: ', 'subsection')
            text_widget.insert('end', f'{explanation}\n', 'body')
        
        text_widget.insert('end', '\nThis arrangement symbolizes:\n', 'body')
        text_widget.insert('end', '• Core traits influence peripheral traits\n', 'bullet')
        text_widget.insert('end', '• The expanding pattern represents growth potential\n', 'bullet')
        text_widget.insert('end', '• No trait exists in isolation - all are interconnected\n', 'bullet')
        
        text_widget.insert('end', '\n' + '─' * 80 + '\n\n', 'separator')
        
        # Personal Insights
        text_widget.insert('end', '💡 PERSONAL INSIGHTS\n', 'section')
        text_widget.insert('end', 'Based on personality psychology research:\n\n', 'body')
        
        if dominant_traits:
            if any(t in ['compassionate', 'empathetic', 'peaceful'] for t, _ in dominant_traits):
                text_widget.insert('end', '▸ Emotional Intelligence Profile:\n', 'subsection')
                text_widget.insert('end', '   High interpersonal orientation ', 'body')
                text_widget.insert('end', '(Goleman, 1995)\n', 'reference')
                text_widget.insert('end', '• Strong capacity for understanding relationships\n', 'bullet')
                text_widget.insert('end', '• Natural prosocial behavior tendency\n\n', 'bullet')
                
            if any(t in ['analytical', 'organized', 'decisive'] for t, _ in dominant_traits):
                text_widget.insert('end', '▸ Systematic Processing Style:\n', 'subsection')
                text_widget.insert('end', '   Executive function strengths ', 'body')
                text_widget.insert('end', '(Stanovich & West, 2000)\n', 'reference')
                text_widget.insert('end', '• Structured problem-solving preference\n', 'bullet')
                text_widget.insert('end', '• High conscientiousness (Big Five)\n\n', 'bullet')
                
            if any(t in ['creative', 'intuitive', 'playful'] for t, _ in dominant_traits):
                text_widget.insert('end', '▸ Openness to Experience:\n', 'subsection')
                text_widget.insert('end', '   Divergent thinking abilities ', 'body')
                text_widget.insert('end', '(McCrae & Costa, 1997)\n', 'reference')
                text_widget.insert('end', '• Enhanced innovation capacity\n', 'bullet')
                text_widget.insert('end', '• Cognitive flexibility\n\n', 'bullet')
                
            if any(t in ['ambitious', 'strong_willed', 'confident'] for t, _ in dominant_traits):
                text_widget.insert('end', '▸ Achievement Orientation:\n', 'subsection')
                text_widget.insert('end', '   High self-efficacy ', 'body')
                text_widget.insert('end', '(Bandura, 1997)\n', 'reference')
                text_widget.insert('end', '• Strong internal locus of control\n', 'bullet')
                text_widget.insert('end', '• Leadership potential\n\n', 'bullet')
        
        text_widget.insert('end', '\n' + '━' * 80 + '\n\n', 'separator')
        
        # References
        text_widget.insert('end', '📖 KEY REFERENCES\n', 'section')
        references = [
            'Arnheim, R. (1974). Art and visual perception.',
            'Bandura, A. (1997). Self-efficacy: The exercise of control.',
            'Costa, P. T., & McCrae, R. R. (1992). NEO-PI-R professional manual.',
            'Deci, E. L., & Ryan, R. M. (2000). Self-determination theory.',
            'Elliot, A. J., & Maier, M. A. (2014). Color psychology.',
            'Goleman, D. (1995). Emotional intelligence.',
            'Jung, C. G. (1964). Man and his symbols.',
            'Peterson, C., & Seligman, M. E. (2004). Character strengths and virtues.',
            'Salovey, P., & Mayer, J. D. (1990). Emotional intelligence framework.',
            'Stanovich, K. E., & West, R. F. (2000). Individual differences in reasoning.'
        ]
        for ref in references:
            text_widget.insert('end', f'• {ref}\n', 'reference')
        
        text_widget.insert('end', '\n' + '━' * 80 + '\n\n', 'separator')
        
        # Footer
        text_widget.insert('end', '✨ Remember: ', 'highlight')
        text_widget.insert('end', 'This visualization represents your self-perception at this moment. ', 'body')
        text_widget.insert('end', 'Character traits can develop and change over time with conscious effort and life experiences.', 'body')
        # Calculate normalized scores
        max_score = 10  # Maximum possible score per trait
        normalized_scores = {trait: score/max_score for trait, score in self.responses.items()}
        
        # Sort traits by score
        sorted_traits = sorted(normalized_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Categorize traits
        dominant_traits = [(t, s) for t, s in sorted_traits if s >= 0.7]
        strong_traits = [(t, s) for t, s in sorted_traits if 0.5 <= s < 0.7]
        moderate_traits = [(t, s) for t, s in sorted_traits if 0.3 <= s < 0.5]
        
        analysis = "CHARACTER PROFILE ANALYSIS\n" + "="*50 + "\n\n"
        
        # Scientific Foundation
        analysis += "SCIENTIFIC FOUNDATION:\n"
        analysis += "This assessment is grounded in established psychological research:\n\n"
        analysis += "• The 20 traits selected integrate findings from:\n"
        analysis += "  - The Big Five personality model (Costa & McCrae, 1992)\n"
        analysis += "  - VIA Character Strengths framework (Peterson & Seligman, 2004)\n"
        analysis += "  - Emotional Intelligence research (Goleman, 1995; Salovey & Mayer, 1990)\n"
        analysis += "  - Self-Determination Theory (Deci & Ryan, 2000)\n\n"
        analysis += "• Each trait represents a dimension validated through decades of research:\n"
        analysis += "  - Cognitive traits (analytical, creative, wise) - linked to intelligence research\n"
        analysis += "  - Emotional traits (empathetic, compassionate) - from emotional intelligence studies\n"
        analysis += "  - Volitional traits (strong-willed, decisive) - from motivation psychology\n"
        analysis += "  - Social traits (loyal, humble) - from interpersonal psychology research\n\n"
        
        # Overview
        analysis += "YOUR PROFILE OVERVIEW:\n"
        analysis += f"Your character profile reveals a unique combination of {len(dominant_traits)} dominant traits, "
        analysis += f"{len(strong_traits)} strong traits, and {len(moderate_traits)} moderate traits.\n\n"
        
        # Dominant traits
        if dominant_traits:
            analysis += "DOMINANT TRAITS (Core Identity):\n"
            analysis += "These shapes appear largest in your visualization, representing your strongest characteristics:\n\n"
            for trait, score in dominant_traits:
                trait_name = trait.replace('_', ' ').title()
                shape = self.trait_info[trait]['shape']
                analysis += f"• {trait_name} ({shape.title()} - {score*100:.0f}% strength)\n"
                analysis += f"  {self.trait_info[trait]['description']}\n"
                analysis += f"  This trait strongly defines how you interact with the world.\n\n"
        
        # Strong traits
        if strong_traits:
            analysis += "\nSTRONG TRAITS (Important Characteristics):\n"
            analysis += "These medium-sized shapes represent significant aspects of your personality:\n\n"
            for trait, score in strong_traits:
                trait_name = trait.replace('_', ' ').title()
                shape = self.trait_info[trait]['shape']
                analysis += f"• {trait_name} ({shape.title()} - {score*100:.0f}% strength)\n"
                analysis += f"  {self.trait_info[trait]['description']}\n\n"
        
        # Visualization explanation
        analysis += "\nVISUALIZATION INTERPRETATION:\n"
        analysis += "Your character visualization uses geometric shapes to represent your personality:\n\n"
        analysis += "• SIZE: Larger shapes indicate stronger traits (based on Gestalt principles of visual hierarchy)\n"
        analysis += "• OPACITY: More solid shapes represent more dominant characteristics\n"
        analysis += "• COLOR: Each color chosen based on color psychology research (Elliot & Maier, 2014)\n"
        analysis += "• POSITION: Shapes are arranged using a modified Fibonacci spiral pattern\n\n"
        
        analysis += "SPATIAL ARRANGEMENT LOGIC:\n"
        analysis += "The geometric shapes are positioned using principles from visual perception research:\n\n"
        analysis += "• SPIRAL PATTERN: Based on the golden spiral found in nature, creating visual harmony\n"
        analysis += "• HIERARCHICAL PLACEMENT: Strongest traits positioned closer to center (attention theory)\n"
        analysis += "• ANGULAR DISTRIBUTION: Shapes spread at 72° intervals to avoid clustering\n"
        analysis += "• PROGRESSIVE DISTANCING: Each subsequent trait placed slightly further out\n"
        analysis += "• This arrangement creates a 'personality mandala' - a balanced, holistic representation\n\n"
        analysis += "The spiral arrangement reflects how personality traits interact:\n"
        analysis += "- Core traits (center) influence and support peripheral traits\n"
        analysis += "- The expanding pattern represents personal growth potential\n"
        analysis += "- No trait exists in isolation - the pattern shows interconnection\n\n"
        
        # Personal insights
        analysis += "PERSONAL INSIGHTS:\n"
        analysis += "Based on personality psychology research, your trait combination suggests:\n\n"
        if dominant_traits:
            if any(t in ['compassionate', 'empathetic', 'peaceful'] for t, _ in dominant_traits):
                analysis += "• High emotional intelligence and interpersonal orientation (Goleman, 1995)\n"
                analysis += "  - Strong capacity for understanding and managing relationships\n"
                analysis += "  - Natural tendency toward prosocial behavior\n"
            if any(t in ['analytical', 'organized', 'decisive'] for t, _ in dominant_traits):
                analysis += "• Systematic processing style and executive function strengths (Stanovich & West, 2000)\n"
                analysis += "  - Preference for structured problem-solving approaches\n"
                analysis += "  - High conscientiousness (Big Five framework)\n"
            if any(t in ['creative', 'intuitive', 'playful'] for t, _ in dominant_traits):
                analysis += "• Openness to experience and divergent thinking abilities (McCrae & Costa, 1997)\n"
                analysis += "  - Enhanced capacity for innovation and novel solutions\n"
                analysis += "  - Flexibility in cognitive processing\n"
            if any(t in ['ambitious', 'strong_willed', 'confident'] for t, _ in dominant_traits):
                analysis += "• High achievement motivation and self-efficacy (Bandura, 1997)\n"
                analysis += "  - Strong internal locus of control\n"
                analysis += "  - Leadership potential and goal-pursuit effectiveness\n"
        
        analysis += "\n" + "="*50 + "\n"
        analysis += "KEY REFERENCES:\n"
        analysis += "• Bandura, A. (1997). Self-efficacy: The exercise of control.\n"
        analysis += "• Costa, P. T., & McCrae, R. R. (1992). NEO-PI-R professional manual.\n"
        analysis += "• Deci, E. L., & Ryan, R. M. (2000). Self-determination theory.\n"
        analysis += "• Elliot, A. J., & Maier, M. A. (2014). Color psychology.\n"
        analysis += "• Goleman, D. (1995). Emotional intelligence.\n"
        analysis += "• Peterson, C., & Seligman, M. E. (2004). Character strengths and virtues.\n"
        analysis += "• Salovey, P., & Mayer, J. D. (1990). Emotional intelligence framework.\n"
        analysis += "• Stanovich, K. E., & West, R. F. (2000). Individual differences in reasoning.\n\n"
        analysis += "="*50 + "\n"
        analysis += "Remember: This visualization represents your self-perception at this moment. "
        analysis += "Character traits can develop and change over time with conscious effort and life experiences."
        
    def create_visualization(self):
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Set background
        ax.add_patch(plt.Rectangle((-10, -10), 20, 20, facecolor='#f0f0f0', alpha=0.3))
        
        # Calculate normalized scores
        max_score = 10
        normalized_scores = {trait: score/max_score for trait, score in self.responses.items()}
        
        # Sort traits by score for better visualization
        sorted_traits = sorted(normalized_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Create a spiral layout for shapes
        num_shapes = len([t for t, s in sorted_traits if s > 0.3])
        
        for i, (trait, score) in enumerate(sorted_traits[:num_shapes]):
            if score > 0.3:
                # Calculate position in a spiral
                angle = i * (2 * np.pi / 5)
                radius = 2 + i * 0.5
                x = radius * np.cos(angle)
                y = radius * np.sin(angle)
                
                # Draw shape based on trait
                color = self.trait_info[trait]['color']
                self.draw_shape(ax, self.trait_info[trait]['shape'], x, y, score, color)
        
        # Add title
        plt.title("Your Unique Character Profile", fontsize=16, fontweight='bold', pad=20)
        
        # Add subtitle explaining arrangement
        plt.text(0, -9, "Shapes arranged in a Fibonacci spiral: strongest traits near center, " +
                "size indicates trait strength", 
                ha='center', fontsize=9, style='italic', color='gray')
        
        # Add subtle grid for reference
        ax.grid(True, alpha=0.1, linestyle='--')
        
        return fig
    
    def draw_shape(self, ax, shape_type, x, y, intensity, color='blue'):
        size = 0.5 + intensity * 1.5
        alpha = 0.3 + intensity * 0.6
        
        if shape_type == 'circle':
            circle = Circle((x, y), size, alpha=alpha, color=color, edgecolor='black', linewidth=0.5)
            ax.add_patch(circle)
            
        elif shape_type == 'square':
            square = Rectangle((x-size/2, y-size/2), size, size, alpha=alpha, color=color,
                             edgecolor='black', linewidth=0.5)
            ax.add_patch(square)
            
        elif shape_type == 'triangle':
            triangle = Polygon([(x, y+size), (x-size*0.866, y-size*0.5), 
                              (x+size*0.866, y-size*0.5)], alpha=alpha, color=color,
                              edgecolor='black', linewidth=0.5)
            ax.add_patch(triangle)
            
        elif shape_type == 'hexagon':
            angles = np.linspace(0, 2*np.pi, 7)
            points = [(x + size*np.cos(a), y + size*np.sin(a)) for a in angles]
            hexagon = Polygon(points, alpha=alpha, color=color, edgecolor='black', linewidth=0.5)
            ax.add_patch(hexagon)
            
        elif shape_type == 'star':
            angles = np.linspace(0, 2*np.pi, 11)
            points = []
            for i, a in enumerate(angles[:-1]):
                r = size if i % 2 == 0 else size * 0.5
                points.append((x + r*np.cos(a), y + r*np.sin(a)))
            star = Polygon(points, alpha=alpha, color=color, edgecolor='black', linewidth=0.5)
            ax.add_patch(star)
            
        elif shape_type == 'diamond':
            diamond = Polygon([(x, y+size), (x-size*0.7, y), (x, y-size), 
                             (x+size*0.7, y)], alpha=alpha, color=color,
                             edgecolor='black', linewidth=0.5)
            ax.add_patch(diamond)
            
        elif shape_type == 'heart':
            t = np.linspace(0, 2*np.pi, 100)
            heart_x = x + size * (16*np.sin(t)**3) / 20
            heart_y = y + size * (13*np.cos(t) - 5*np.cos(2*t) - 2*np.cos(3*t) - np.cos(4*t)) / 20
            ax.fill(heart_x, heart_y, alpha=alpha, color=color, edgecolor='black', linewidth=0.5)
            
        elif shape_type == 'spiral':
            theta = np.linspace(0, 4*np.pi, 100)
            r = np.linspace(0, size, 100)
            spiral_x = x + r * np.cos(theta)
            spiral_y = y + r * np.sin(theta)
            ax.plot(spiral_x, spiral_y, alpha=alpha, color=color, linewidth=3)
            
        elif shape_type == 'oval':
            oval = mpatches.Ellipse((x, y), size*1.5, size, alpha=alpha, color=color,
                                   edgecolor='black', linewidth=0.5)
            ax.add_patch(oval)
            
        elif shape_type == 'arrow':
            arrow = mpatches.FancyArrowPatch((x, y-size), (x, y+size),
                                           arrowstyle='->', mutation_scale=20*size,
                                           alpha=alpha, color=color, edgecolor='black')
            ax.add_patch(arrow)
            
        elif shape_type == 'pentagon':
            angles = np.linspace(0, 2*np.pi, 6)
            points = [(x + size*np.cos(a-np.pi/2), y + size*np.sin(a-np.pi/2)) for a in angles]
            pentagon = Polygon(points[:-1], alpha=alpha, color=color, edgecolor='black', linewidth=0.5)
            ax.add_patch(pentagon)
            
        elif shape_type == 'crescent':
            arc = Wedge((x, y), size, 30, 330, alpha=alpha, color=color, edgecolor='black', linewidth=0.5)
            ax.add_patch(arc)
            
        elif shape_type == 'sun':
            # Central circle
            sun = Circle((x, y), size*0.5, alpha=alpha, color=color, edgecolor='black', linewidth=0.5)
            ax.add_patch(sun)
            # Rays
            for angle in np.linspace(0, 2*np.pi, 12, endpoint=False):
                ray_x = [x + size*0.5*np.cos(angle), x + size*np.cos(angle)]
                ray_y = [y + size*0.5*np.sin(angle), y + size*np.sin(angle)]
                ax.plot(ray_x, ray_y, alpha=alpha, color=color, linewidth=2)
                
        elif shape_type == 'wave':
            wave_x = np.linspace(x-size, x+size, 100)
            wave_y = y + size*0.3*np.sin(4*np.pi*(wave_x-x)/size)
            ax.plot(wave_x, wave_y, alpha=alpha, color=color, linewidth=3)
            
        elif shape_type == 'shield':
            shield_points = [(x, y+size), (x-size*0.7, y+size*0.5), (x-size*0.7, y-size*0.3),
                           (x, y-size), (x+size*0.7, y-size*0.3), (x+size*0.7, y+size*0.5)]
            shield = Polygon(shield_points, alpha=alpha, color=color, edgecolor='black', linewidth=0.5)
            ax.add_patch(shield)
            
        elif shape_type == 'eye':
            # Eye shape
            eye_x = np.linspace(x-size, x+size, 100)
            eye_upper = y + size*0.5*np.sqrt(1-(eye_x-x)**2/size**2)
            eye_lower = y - size*0.5*np.sqrt(1-(eye_x-x)**2/size**2)
            ax.fill_between(eye_x, eye_lower, eye_upper, alpha=alpha, color=color, edgecolor='black', linewidth=0.5)
            # Pupil
            pupil = Circle((x, y), size*0.3, alpha=1, color='black')
            ax.add_patch(pupil)
            
        elif shape_type == 'grid':
            # Draw a grid pattern
            for i in range(3):
                ax.plot([x-size/2+i*size/2, x-size/2+i*size/2], [y-size/2, y+size/2], 
                       alpha=alpha, color=color, linewidth=2)
                ax.plot([x-size/2, x+size/2], [y-size/2+i*size/2, y-size/2+i*size/2], 
                       alpha=alpha, color=color, linewidth=2)
                       
        elif shape_type == 'question':
            # Draw a question mark
            t = np.linspace(0, 1.5*np.pi, 50)
            q_x = x + size*0.3*np.cos(t+np.pi/2)
            q_y = y + size*0.3 + size*0.3*np.sin(t+np.pi/2)
            ax.plot(q_x, q_y, alpha=alpha, color=color, linewidth=3)
            # Dot
            dot = Circle((x, y-size*0.3), size*0.1, alpha=alpha, color=color)
            ax.add_patch(dot)
            
        elif shape_type == 'line':
            ax.plot([x-size, x+size], [y, y], alpha=alpha, color=color, linewidth=4)
            
        elif shape_type == 'small_circle':
            circle = Circle((x, y), size*0.5, alpha=alpha, color=color, edgecolor='black', linewidth=0.5)
            ax.add_patch(circle)
            
        else:  # Default to circle
            circle = Circle((x, y), size*0.7, alpha=alpha, color='gray', edgecolor='black', linewidth=0.5)
            ax.add_patch(circle)
    
    def save_visualization(self, fig):
        fig.savefig('my_character_visualization.png', dpi=300, bbox_inches='tight')
        messagebox.showinfo("Success", "Image saved as 'my_character_visualization.png'")
    
    def restart(self):
        self.current_question = 0
        self.responses = {trait: 0 for trait in self.trait_info}
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.setup_ui()

if __name__ == "__main__":
    root = tk.Tk()
    app = CharacterVisualizationApp(root)
    root.mainloop()