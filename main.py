import json
import click

@click.group("zapp")
def zapp():
    print("running zapper")

def main():
    zapp()

if __name__=="__main__":
    main()