
from serial import Serial

class ModbusAsciiRequest:

    def __init__(self,  *args, **kwargs):
        frame_data = kwargs['data'].upper()
        if frame_data[0] == ':':
            frame_data = frame_data[1:]
        if len(frame_data) == 14:
            self.__address_chennal = frame_data[0:2]
            self.__function_index = frame_data[2:4]
            self.__first_register = frame_data[4:8]
            self.__total_number = frame_data[8:12]
            self.__check_error = frame_data[12:14]
            self.__data_frame = ':' + frame_data + '\n\r'
        elif len(frame_data) == 12:
            self.__address_chennal = frame_data[0:2]
            self.__function_index = frame_data[2:4]
            self.__first_register = frame_data[4:8]
            self.__total_number = frame_data[8:12]
            self.__check_error = self.calculate_lrc(frame_data[0:12])
            self.__data_frame = ':' + frame_data + self.__check_error + '\n\r'

        else:
            raise ("The data frame is error !")

    @classmethod
    def SetByString(cls,*args, **kwargs):
        add = kwargs['address']
        func = kwargs['function']
        fir_res = kwargs['first_register']
        total = kwargs['total_number']
        return cls(data=add+func+fir_res+total)

    @classmethod
    def SetByStringList(cls, *args, **kwargs):
        data = args[0]+args[1]+args[2]+args[3]
        return cls(data=data)

    @classmethod
    def SetByHex(cls, *args, **kwargs):
        add = format(kwargs['address'], "02x")
        func = format(kwargs['function'], "02x")
        fir_res = format(kwargs['first_register'], "04x")
        total = format(kwargs['total_number'], "04x")
        return cls(data=add + func + fir_res + total)

    @staticmethod
    def calculate_lrc(frame_data):
        result_lrc = 0x00
        frame_data = frame_data.lower()
        for fir_txt, sec_txt in zip(frame_data[::2], frame_data[1::2]):
            byte_of_tring = fir_txt + sec_txt
            result_lrc += int(byte_of_tring, 16)
        result_lrc = 0xff - result_lrc + 1
        return hex(result_lrc)[2:].upper()

    @property
    def DataFrame(self):
        return self.__data_frame

    @property
    def Address(self):
        return self.__address_chennal

    @property
    def Function(self):
        return self.__function_index

    @property
    def TotalNumber(self):
        return self.__total_number

    @property
    def FristRegister(self):
        return self.__first_register

    @property
    def CheckLRC(self):
        return self.__check_error

    def put(self, connect):
        if connect.is_open:
            connect.write(self.__data_frame.encode())
        else:
            raise ("The connect is fail !!")

class ModbusRtuRequest:

    def __init__(self,  *args, **kwargs):

        self.__start_signal = kwargs['start']
        self.__stop_signal = kwargs['stop']
        frame_data = kwargs['data']
        if len(frame_data) == 16:
            self.__address_chennal = frame_data[0:2]
            self.__function_index = frame_data[2:4]
            self.__first_register = frame_data[4:8]
            self.__total_number = frame_data[8:12]
            self.__check_error = frame_data[12:16]
            self.__data_frame = self.__start_signal + frame_data + self.__stop_signal
        elif len(frame_data) == 12:
            self.__address_chennal = frame_data[0:2]
            self.__function_index = frame_data[2:4]
            self.__first_register = frame_data[4:8]
            self.__total_number = frame_data[8:12]
            self.__check_error = self.calculate_crc(frame_data[0:12])
            self.__data_frame = frame_data + self.__check_error
            self.__total_date_frame = self.__start_signal + frame_data + self.__check_error + self.__stop_signal
        else:
            raise ("The data frame is error !")

    @staticmethod
    def _initial(c,POLYNOMIAL):
        crc = 0
        c = c << 8
        for j in range(8):
            if (crc ^ c) & 0x8000:
                crc = (crc << 1) ^ POLYNOMIAL
            else:
                crc = crc << 1
            c = c << 1
        return crc

    @staticmethod
    def _update_crc(crc, c, POLYNOMIAL):
        cc = 0xff & c
        _tab = [ModbusRtuRequest._initial(i, POLYNOMIAL) for i in range(256)]
        tmp = (crc >> 8) ^ cc
        crc = (crc << 8) ^ _tab[tmp & 0xff]
        crc = crc & 0xffff
        return crc

    @staticmethod
    def calculate_crc(frame_data,POLYNOMIAL = 0x1021, PRESET= 0):
        crc = PRESET
        frame_data = frame_data.lower()
        for c in frame_data:
            crc = ModbusRtuRequest._update_crc(crc, ord(c),POLYNOMIAL)
        return hex(crc)[2:].upper()

    def put(self,connect):
        if connect.is_open:
            connect.write(self.__start_signal.encode())
            connect.write(bytes.fromhex(self.__data_frame))
            connect.write(self.__stop_signal.encode())
        else:
            raise ("The connect is fail !!")

    @property
    def DataFrame(self):
        return self.__data_frame

    @property
    def Address(self):
        return self.__address_chennal

    @property
    def Function(self):
        return self.__function_index

    @property
    def TotalNumber(self):
        return self.__total_number

    @property
    def FristRegister(self):
        return self.__first_register

    @property
    def CheckCRC(self):
        return self.__check_error

if __name__ == "__main__":

    data = '0606006B0003'
    #data_frame = ModbusAsciiRequest.SetByString(address= '06',function= '06', first_register = '006b', total_number = '0003')
    data_frame = ModbusAsciiRequest.SetByStringList('06','06','006b','0003')

    with Serial('COM2', 9600) as connect_serial:
        data_frame.put(connect_serial)