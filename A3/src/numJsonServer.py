#!/usr/bin/env python3

import socket
import a2


def main():
    # Connect to socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        PORT = 8000
        s.bind(("127.0.0.1", PORT))
        s.listen()
        print('Listening on port %d' % PORT)
        conn, address = s.accept()

        data = ''

        while True:
            data += ' ' + conn.recv(8192).decode('utf-8').strip()
            if data.strip().endswith('END'):
                dataLenTillEnd = len(data) - 3
                data = data[:dataLenTillEnd]
                break

        parsedInputList = a2.delimSplit(data)
        parsedNumJsons = a2.parseNumJsons(parsedInputList, '--sum')

        response = str(parsedNumJsons) + '\n'

        conn.send(response.encode('utf-8'))
    except OSError:
        conn.close()
        print('We have encountered an OSError :(')
    except UnicodeDecodeError:
        print('We have encountered an invalid character or SIGINT :(')
        conn.close()
    except KeyboardInterrupt:
        print('We have encountered a KeyboardInterrupt error :(')
        s.close()
    except socket.error as e:
        print('We have encountered the following socket error :( \n %s' % e)


if __name__ == '__main__':
    main()
