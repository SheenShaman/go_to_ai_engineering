from app.llm import ask_llm

def main():
    answer = ask_llm(
        "What can you do?",
    )
    print(answer)


if __name__ == "__main__":
    main()
