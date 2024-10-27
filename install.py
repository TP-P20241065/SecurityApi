import subprocess

def install_requirements():
    subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
    subprocess.run(["prisma", "generate"], check=True)

if __name__ == "__main__":
    install_requirements()
