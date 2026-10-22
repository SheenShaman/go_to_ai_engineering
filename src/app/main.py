from app.agent import run_agent


def main():
    history = []

    while True:
        user_message = input("\nТы: ").strip()

        if user_message.lower() in {"exit", "quit"}:
            break

        if not user_message:
            continue

        print("Агент: ", end="", flush=True)

        try:
            run_agent(
                user_message,
                history,
                stream=False,
                structured=False,
            )
            print()

        except Exception as error:
            print(f"\nОшибка: {error}")


if __name__ == "__main__":
    main()
