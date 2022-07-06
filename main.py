from publish import publish_to_mqtt

## Needs LGHUB from Logitech installed and running

#
# This program reads the info provided by LGHUB
#
# - reads battery information from sqlite db stored by LGHUB
# - reports battery status to mqtt
#

def main():
    publish_to_mqtt()

if __name__ == '__main__':
    main()