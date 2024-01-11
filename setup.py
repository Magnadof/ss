import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["flask", "pandas"],  # Adicione outras dependências do seu projeto aqui
    "includes": ["servidor"],
    "include_files": [
        ("static", "static"),  # Inclui a pasta 'static' e todo o seu conteúdo
        ("templates", "templates"),  # Inclui a pasta 'templates' e todo o seu conteúdo
        ("bank", "bank"),
        ('env', 'env')
    ]
}

executables = [Executable("servidor.py", base=None)]

setup(
    name="servidor",
    version="1.0",
    description="Servidor de gerenciamento de dados",
    options={"build_exe": build_exe_options},
    executables=executables
)
