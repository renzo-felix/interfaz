import serial
import time
import datetime

class Data:
    def __init__(self, port, baudrate=9600,team_id="1000"):
        self.port = port
        self.baudrate = baudrate
        self.serial = serial.Serial(port=self.port, baudrate=self.baudrate)
        self.TeamID_list = []
        self.Mission_time = []
        self.packetcount_list = []
        self.altitud_list = []
        self.temperature_list = []
        self.ang_x_list = []
        self.ang_y_list = []
        self.voltage_list = []
        self.pressure_list = []
        self.MODE_list = []
        self.STATE_list = []
        self.team_id=team_id
        self.HS_DEPLOYED_list = []
        self.PC_DEPLOYED_list = []
        self.MAST_RAISED_list = []
        self.GPS_TIME_list = []
        self.GPS_ALTITUDE_list = []
        self.GPS_LATITUDE_list = [] 
        self.GPS_LONGITUD_list = []
        self.GPS_SATS_list = []
        self.CMD_ECHO_list = []

    def read(self):
        return self.serial.readline().decode().strip()

    def send(self, data):
        data = str(data).encode()
        self.serial.write(data)

    def close(self):
        self.serial.close()

    def parse_data(self, data):
        data_list = data.split(',')
        TeamID, missiontime,packetcount,MODE,STATE, altitud,HS_DEPLOYED,PC_DEPLOYED,MAST_RAISED, temperatura,bateria, GPS_TIME,GPS_ALTITUDE,GPS_LATITUDE,GPS_LONGITUD,GPS_SATS,ang_x, ang_y, CMD_ECHO,pressure = data_list
        self.TeamID_list.append(int(TeamID))
        self.Mission_time.append(missiontime)
        self.packetcount_list.append(int(packetcount))
        self.MODE_list.append(MODE)
        self.STATE_list.append(STATE)
        self.altitud_list.append(float(altitud))
        self.HS_DEPLOYED_list.append(HS_DEPLOYED)
        self.PC_DEPLOYED_list.append(PC_DEPLOYED)
        self.MAST_RAISED_list.append(MAST_RAISED)
        self.temperature_list.append(float(temperatura))
        self.voltage_list.append(float(bateria))
        self.GPS_TIME_list.append(GPS_TIME)
        self.GPS_ALTITUDE_list.append(GPS_ALTITUDE)
        self.GPS_LATITUDE_list.append(GPS_LATITUDE)
        self.GPS_LONGITUD_list.append(GPS_LONGITUD)
        self.GPS_SATS_list.append(GPS_SATS)
        self.ang_x_list.append(float(ang_x))
        self.ang_y_list.append(float(ang_y))
        self.CMD_ECHO_list.append(CMD_ECHO)
        self.pressure_list.append(float(pressure))
        
    def simulate(self,ENABLE=True):
        if ENABLE:
            # Enviar el comando "ENABLE"
            enable_command = f"CMD,{self.team_id},SIM,ENABLE\n"
        else:
            enable_command = f"CMD,{self.team_id},SIM,DISABLE\n"
        self.send(enable_command)
    def SIMP_pressure(self):
        altitudes = list(range(1000, -1, -1))
        P0 = 1013.25
        pressures = [(1 - altitudes/145366.45)*P0 for altitude in altitudes]
        for pressure in pressures:
            command = f"CMD,{self.team_id},SIMP,{pressure}\n"
    def telemetry(self,ON_OFF="ON"):
        activate_command = f"CMD,{self.team_id},CX,{ON_OFF}\n"
        self.send(activate_command)
    def SetTime(self,GPS=False):
        if not(GPS):
            now = datetime.datetime.now()
            set_command=f"CMD,{self.team_id},ST,{now}\n"
        else:
            set_command=f"CMD,{self.team_id},ST,GPS\n"
        self.send(set_command)
    def CalibrateAltitude(self):
        cal_command = f"CMD,{self.team_id},CAL\n"
        self.send(cal_command)
    def AudioCommand(self,ON_OFF="ON"):
        activate_command = f"CMD,{self.team_id},BCN,{ON_OFF}\n"
        self.send(activate_command)