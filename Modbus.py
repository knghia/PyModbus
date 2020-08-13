from serial import Serial
import numpy as np

class ModbusAsciiRequest:

    def __init__(self,frame_data):

        if frame_data[0] == ':':
            frame_data = frame_data[1:]
        if len(frame_data) == 14:
            self.__address_chennal = frame_data[0:2]
            self.__function_index = frame_data[2:4]
            self.__first_register = frame_data[4:8]
            self.__total_number = frame_data[8:12]
            self.__check_lrc = frame_data[12:14]
            self.__data_frame = ':'+frame_data+'\n\r'
        elif len(frame_data) == 12:
            self.__address_chennal = frame_data[0:2]
            self.__function_index = frame_data[2:4]
            self.__first_register = frame_data[4:8]
            self.__total_number = frame_data[8:12]
            self.__check_lrc = self.calculate_lrc(frame_data[0:12])
            self.__data_frame = ':'+frame_data+self.__check_lrc+'\n\r'

        else:
            raise("The data frame is error !")
    
    @staticmethod
    def calculate_lrc(frame_data):
        result_lrc = 0x00
        for fir_txt,sec_txt in zip(frame_data[::2], frame_data[1::2]):
            byte_of_tring = fir_txt+sec_txt
            result_lrc += int(byte_of_tring,16)
        result_lrc = 0xff - result_lrc + 1
        return hex(result_lrc)[2:]
    
    def print(self):
        print(self.__data_frame)

    @property
    def DataFrame(self):
        return self.__data_frame

    def put(self,connect):
        if connect_serial.is_open:
            connect_serial.write(self.__data_frame.encode())
        else:
            raise("The connect is fail !!")

if __name__ == "__main__":
    
    data = ':0606006b0003'
    data_frame = ModbusAsciiRequest(data)
    print(data_frame.DataFrame)

    with Serial('COM2',9600) as connect_serial:
        data_frame.put(connect_serial)