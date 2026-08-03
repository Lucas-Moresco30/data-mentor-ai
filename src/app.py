import sys

from chatbot import ChatBot


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stdin, "reconfigure"):
        sys.stdin.reconfigure(encoding="utf-8")

    print("=" * 50)
    print("🤖 Data Mentor AI")
    print("=" * 50)
    bot = ChatBot(debug=False)
    print("\nBase de conhecimento carregada!")

    while True:
        pergunta = input("\nVocê: ").strip()
        if pergunta.lower() in {"sair", "exit", "quit"}:
            print("\nAté logo!")
            break
        print("\nAssistente:\n")
        print(bot.responder(pergunta))


if __name__ == "__main__":
    main()
