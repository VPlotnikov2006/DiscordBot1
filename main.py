from dotenv import dotenv_values

if __name__ == "__main__":
    print(dotenv_values(".env")["API_TOKEN"])