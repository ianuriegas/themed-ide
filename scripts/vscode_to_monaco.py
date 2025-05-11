import json
import os
from pathlib import Path

def map_terminal_to_editor_colors(vscode_colors):
    """Map VS Code terminal colors to Monaco editor colors."""
    color_mapping = {
        'terminal.foreground': 'editor.foreground',
        'terminal.background': 'editor.background',
        'terminal.selectionBackground': 'editor.selectionBackground',
        'terminalCursor.foreground': 'editorCursor.foreground',
    }
    
    monaco_colors = {}
    for vscode_key, monaco_key in color_mapping.items():
        if vscode_key in vscode_colors:
            monaco_colors[monaco_key] = vscode_colors[vscode_key]
    
    # Add some default Monaco-specific colors if not present
    if 'editor.lineHighlightBackground' not in monaco_colors:
        monaco_colors['editor.lineHighlightBackground'] = '#00000012'
    if 'editorWhitespace.foreground' not in monaco_colors:
        monaco_colors['editorWhitespace.foreground'] = '#BFBFBF'
    
    return monaco_colors

def create_syntax_rules(vscode_colors):
    """Create Monaco syntax highlighting rules based on VS Code colors."""
    rules = []
    
    # Map ANSI colors to syntax tokens with simplified coverage
    ansi_to_token = {
        # Basic syntax elements
        'terminal.ansiRed': [
            'keyword', 'storage', 'storage.type',
            'keyword.control', 'keyword.operator',
            # Type system
            'keyword.type', 'keyword.interface',
            'keyword.class', 'keyword.enum',
            # Language-specific keywords
            'keyword.import', 'keyword.package',
            'keyword.namespace', 'keyword.using'
        ],
        'terminal.ansiGreen': [
            'string', 'string.quoted',
            'string.quoted.single', 'string.quoted.double',
            'string.quoted.triple', 'string.template',
            # Language-specific strings
            'string.regexp', 'string.quoted.raw',
            'string.quoted.docstring'
        ],
        'terminal.ansiYellow': [
            'comment', 'comment.line', 'comment.block',
            'comment.documentation'
        ],
        'terminal.ansiBlue': [
            'variable', 'variable.parameter',
            'variable.other', 'variable.other.property',
            'variable.other.object', 'variable.other.constant'
        ],
        'terminal.ansiMagenta': [
            'entity.name.function', 'entity.name.method',
            'entity.name.class', 'entity.name.type',
            'entity.name.tag', 'entity.other.attribute-name'
        ],
        'terminal.ansiCyan': [
            'constant', 'constant.numeric',
            'constant.language', 'constant.character',
            'constant.other', 'constant.numeric.integer',
            'constant.numeric.float', 'constant.numeric.hex'
        ],
        'terminal.ansiWhite': [
            'text', 'text.plain',
            'text.xml', 'text.html',
            'text.css', 'text.javascript'
        ],
        # Bright variants for emphasis
        'terminal.ansiBrightRed': [
            'invalid', 'invalid.illegal',
            'invalid.deprecated'
        ],
        'terminal.ansiBrightGreen': [
            'string.regexp', 'string.quoted.regexp',
            'string.quoted.regexp.heredoc'
        ],
        'terminal.ansiBrightYellow': [
            'markup.heading', 'markup.underline',
            'markup.underline.link', 'markup.bold',
            'markup.italic'
        ],
        'terminal.ansiBrightBlue': [
            'support', 'support.function',
            'support.class', 'support.type',
            'support.constant'
        ],
        'terminal.ansiBrightMagenta': [
            'entity.name.namespace',
            'entity.name.scope-resolution',
            'entity.name.label'
        ],
        'terminal.ansiBrightCyan': [
            'constant.character.escape',
            'constant.character.entity',
            'constant.character.unicode'
        ],
        'terminal.ansiBrightWhite': [
            'meta', 'meta.preprocessor',
            'meta.selector', 'meta.tag',
            'meta.type.annotation'
        ]
    }
    
    # Create rules for each token type
    for ansi_key, tokens in ansi_to_token.items():
        if ansi_key in vscode_colors:
            color = vscode_colors[ansi_key].lstrip('#')
            for token in tokens:
                rules.append({
                    'foreground': color,
                    'token': token
                })
    
    # Add special rules for specific language features
    if 'terminal.ansiRed' in vscode_colors:
        rules.extend([
            {
                'foreground': vscode_colors['terminal.ansiRed'].lstrip('#'),
                'token': 'keyword.operator.logical'
            },
            {
                'foreground': vscode_colors['terminal.ansiRed'].lstrip('#'),
                'token': 'keyword.operator.arithmetic'
            }
        ])
    
    if 'terminal.ansiGreen' in vscode_colors:
        rules.extend([
            {
                'foreground': vscode_colors['terminal.ansiGreen'].lstrip('#'),
                'token': 'string.template'
            },
            {
                'foreground': vscode_colors['terminal.ansiGreen'].lstrip('#'),
                'token': 'string.quoted.template'
            }
        ])
    
    if 'terminal.ansiBlue' in vscode_colors:
        rules.extend([
            {
                'foreground': vscode_colors['terminal.ansiBlue'].lstrip('#'),
                'token': 'variable.other.readwrite.global'
            },
            {
                'foreground': vscode_colors['terminal.ansiBlue'].lstrip('#'),
                'token': 'variable.other.readwrite.local'
            }
        ])
    
    return rules

def convert_vscode_to_monaco(vscode_theme_path, output_dir):
    """Convert a VS Code theme to Monaco format."""
    with open(vscode_theme_path, 'r') as f:
        vscode_theme = json.load(f)
    
    # Extract colors from VS Code theme
    vscode_colors = vscode_theme.get('workbench.colorCustomizations', {})
    
    # Create Monaco theme
    monaco_theme = {
        'base': 'vs-dark' if 'dark' in vscode_theme_path.lower() else 'vs',
        'inherit': True,
        'rules': create_syntax_rules(vscode_colors),
        'colors': map_terminal_to_editor_colors(vscode_colors)
    }
    
    # Create output filename (without _monaco suffix)
    output_filename = Path(vscode_theme_path).stem + '.json'
    output_path = os.path.join(output_dir, output_filename)
    
    # Write Monaco theme
    with open(output_path, 'w') as f:
        json.dump(monaco_theme, f, indent=2)
    
    return output_path

def main():
    # Create output directory if it doesn't exist
    output_dir = 'monaco_themes'
    os.makedirs(output_dir, exist_ok=True)
    
    # Get all VS Code themes
    vscode_themes_dir = 'iTerm2-Color-Schemes/vscode'
    for theme_file in os.listdir(vscode_themes_dir):
        if theme_file.endswith('.json'):
            vscode_theme_path = os.path.join(vscode_themes_dir, theme_file)
            output_path = convert_vscode_to_monaco(vscode_theme_path, output_dir)
            print(f'Converted {theme_file} to {output_path}')

if __name__ == '__main__':
    main() 