import os

directories = [
    'src/agents',
    'src/crew',
    'src/tools',
    'src/data',
    'src/rag',
    'src/models',
    'src/scoring',
    'src/config',
    'ui',
    'data/cache',
    'data/vectordb',
    'data/sample_transcripts',
    'tests/test_tools',
    'tests/test_agents',
    'tests/test_scoring',
    'notebooks',
    'docs'
]

for directory in directories:
    os.makedirs(directory, exist_ok=True)
    print(f'Created: {directory}')

print(f'\nTotal directories created/verified: {len(directories)}')
