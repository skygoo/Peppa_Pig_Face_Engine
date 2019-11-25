import socket

from face_tracker import Marker


class MayaSocket:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("start connect....")
        self.socket.connect(('10.1.120.70', 5055))
        print("connect success....")
        self.modifier = 1.4

    def transMelCmd(self, name, pos):
        return "setAttr " + name + ".translateX " + str(
            pos[0] * self.modifier) + ";\n setAttr " + name + ".translateY " + str(
            -pos[1] * self.modifier) + ";\n"

    def send(self, markers):
        # cmd = "currentTime (`currentTime -query` + 1);\n"
        #
        # cmd += self.transMelCmd("lob", markers[Marker.LEFTOUTERBROW.value])
        # cmd += self.transMelCmd("lib", markers[Marker.LEFTINNERBROW.value])
        # cmd += self.transMelCmd("rib", markers[Marker.RIGHTINNERBROW.value])
        # cmd += self.transMelCmd("rob", markers[Marker.RIGHTOUTERBROW.value])
        # cmd += self.transMelCmd("lc", markers[Marker.LEFTCHEEK.value])
        # cmd += self.transMelCmd("rc", markers[Marker.RIGHTCHEEK.value])
        # cmd += self.transMelCmd("ln", markers[Marker.LEFTNOSE.value])
        # cmd += self.transMelCmd("rn", markers[Marker.RIGHTNOSE.value])
        # cmd += self.transMelCmd("ul", markers[Marker.UPPERLIP.value])
        # cmd += self.transMelCmd("lm", markers[Marker.LEFTMOUTH.value])
        # cmd += self.transMelCmd("rm", markers[Marker.RIGHTMOUTH.value])
        # cmd += self.transMelCmd("ll", markers[Marker.LOWERLIP.value])
        # print(cmd)

        # cmd += "setKeyframe lob lib rib rob lc rc ln rn lm ul rm ll;\n"

        # self.socket.sendall(bytes(cmd, 'utf8'))
        self.socket.sendall(bytes(self.transMelCmd("lob", markers[Marker.LEFTOUTERBROW.value]), 'utf8'))
        self.socket.sendall(bytes(self.transMelCmd("lib", markers[Marker.LEFTINNERBROW.value]), 'utf8'))
        self.socket.sendall(bytes(self.transMelCmd("rib", markers[Marker.RIGHTINNERBROW.value]), 'utf8'))
        self.socket.sendall(bytes(self.transMelCmd("rob", markers[Marker.RIGHTOUTERBROW.value]), 'utf8'))
        self.socket.sendall(bytes(self.transMelCmd("lc", markers[Marker.LEFTCHEEK.value]), 'utf8'))
        self.socket.sendall(bytes(self.transMelCmd("rc", markers[Marker.RIGHTCHEEK.value]), 'utf8'))
        self.socket.sendall(bytes(self.transMelCmd("ln", markers[Marker.LEFTNOSE.value]), 'utf8'))
        self.socket.sendall(bytes(self.transMelCmd("rn", markers[Marker.RIGHTNOSE.value]), 'utf8'))
        self.socket.sendall(bytes(self.transMelCmd("ul", markers[Marker.UPPERLIP.value]), 'utf8'))
        self.socket.sendall(bytes(self.transMelCmd("lm", markers[Marker.LEFTMOUTH.value]), 'utf8'))
        self.socket.sendall(bytes(self.transMelCmd("rm", markers[Marker.RIGHTMOUTH.value]), 'utf8'))
        self.socket.sendall(bytes(self.transMelCmd("ll", markers[Marker.LOWERLIP.value]), 'utf8'))
