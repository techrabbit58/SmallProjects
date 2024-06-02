from http.client import HTTPSConnection


def main():
    conn = HTTPSConnection('inventwithpython.com')
    conn.request('GET', '/bitmapworld.txt')
    resp = conn.getresponse()
    print(resp.status, resp.reason)
    with open('small_projects/03_bitmap_message/_bitmapworld.py', 'w') as f:
        f.write('BITMAP = [\n')
        for line in resp.readlines():
            f.write(f'    "{line.decode().strip('\n\r')}",\n')
        f.write(']')
    resp.close()
    conn.close()


if __name__ == '__main__':
    main()
