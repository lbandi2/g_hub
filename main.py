from utils import make_dir
from publish import publish_to_mqtt

## Needs https://github.com/andyvorld/LGSTrayBattery installed and running

def main():
    make_dir('data')
    publish_to_mqtt()

if __name__ == '__main__':
    main()