try:
    from .app import main
except SystemError:
    from app import main

main()