sudo apt update
sudo apt install pipx
pipx install poetry
poetry completions bash >> ~/.bash_completion

git clone https://github.com/yuragorlo/token-analysis.git
cd token-analysis
cp .env.example .env
nano .env ... amd put your api keys

poetry install --no-root
poetry shell

python main.py