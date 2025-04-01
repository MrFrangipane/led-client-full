

if __name__ == "__main__":
    import math
    import time

    from stupidArtnet import StupidArtnet

    target_node = "192.168.20.201"
    fps = 30
    segments = [
        {"u": 3, "s": [
            {"p": [0, 63], "c": [255, 0, 0]},
            {"p": [64, 127], "c": [255, 255, 0]}
        ]},
        {"u": 4, "s": [
            {"p": [0, 63], "c": [0, 255, 0]},
            {"p": [64, 127], "c": [0, 255, 255]}
        ]},
        {"u": 5, "s": [
            {"p": [0, 127], "c": [0, 0, 255]}
        ]}
    ]

    clients = dict()
    universes = dict()
    for universe in segments:
        universe_number = universe['u']
        stupid_artnet = StupidArtnet(target_ip=target_node, universe=universe_number, fps=fps)
        stupid_artnet.start()
        clients[universe_number] = stupid_artnet

        universes[universe_number] = bytearray(512)

    running = True
    while running:
        try:
            for universe in segments:
                universe_number = universe['u']

                for segment in universe['s']:
                    for p in range(segment['p'][0], segment['p'][1] + 1):
                        factor = math.sin(time.time() * 3 + p) * 0.5 + 0.5
                        if factor < 0.5:
                            factor = 0

                        for i in range(3):
                            universes[universe_number][p * 3 + i] = int(segment['c'][i] * factor)

                client = clients[universe_number]
                client.set(universes[universe_number])

            time.sleep(1.0 / float(fps))

        except KeyboardInterrupt:
            running = False
