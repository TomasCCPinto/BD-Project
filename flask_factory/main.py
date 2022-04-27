import __init__ as init
#modules

def main():
    """
    the core of API Rest 
    """

    app = init.creat_app()
    app.run(debug=True)


if __name__ == "__main__":
    main()