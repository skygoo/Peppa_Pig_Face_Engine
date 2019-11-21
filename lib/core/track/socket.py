import socket
from enum import Enum


class Marker(Enum):
    LEFTOUTERBROW = 1
    LEFTINNERBROW = 2
    RIGHTINNERBROW = 3
    RIGHTOUTERBROW = 4
    LEFTCHEEK = 5
    RIGHTCHEEK = 6
    LEFTNOSE = 7
    NOSE = 8
    RIGHTNOSE = 9
    UPPERLIP = 10
    LEFTMOUTH = 11
    RIGHTMOUTH = 12
    LOWERLIP = 13


class MayaSocket:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("start connect....")
        self.socket.connect(('127.0.0.1', 8088))
        print("connect success....")
        self.modifier = 1.4

    def transMelCmd(self, name, pos):
        return "setAttr " + name + ".translateX " + pos.x * self.modifier + ";\n setAttr " + name + ".translateY " + (
                -pos.y * self.modifier) + ";\n"

    def send(self, markers):
        cmd = "currentTime (`currentTime -query` + 1);\n"

        cmd += self.transMelCmd("lob", markers[Marker.LEFTOUTERBROW])
        cmd += self.transMelCmd("lib", markers[Marker.LEFTINNERBROW])
        cmd += self.transMelCmd("rib", markers[Marker.RIGHTINNERBROW])
        cmd += self.transMelCmd("rob", markers[Marker.RIGHTOUTERBROW])
        cmd += self.transMelCmd("lc", markers[Marker.LEFTCHEEK])
        cmd += self.transMelCmd("rc", markers[Marker.RIGHTCHEEK])
        cmd += self.transMelCmd("ln", markers[Marker.LEFTNOSE])
        cmd += self.transMelCmd("rn", markers[Marker.RIGHTNOSE])
        cmd += self.transMelCmd("ul", markers[Marker.UPPERLIP])
        cmd += self.transMelCmd("lm", markers[Marker.LEFTMOUTH])
        cmd += self.transMelCmd("rm", markers[Marker.RIGHTMOUTH])
        cmd += self.transMelCmd("ll", markers[Marker.LOWERLIP])

        # cmd += "setKeyframe lob lib rib rob lc rc ln rn lm ul rm ll;\n"

        self.socket.send(bytes(cmd))
