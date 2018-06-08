

from dynamixel_sdk import *

class DynamixelServomotorController:

    """This is a comment about this ww """

    # 
    # @param device_name: 
    #  USD device name. Usually it is ttyUSB0
    # @param protoco_version: 
    # @param baudrate:
    # @motor_config:
    def __init__(self, device_name, protocol_version, baudrate, motor_config):
        self.initialized = True
        self.port_handler = PortHandler(device_name)
        self.packet_handler = PacketHandler(protocol_version)
        self.motor_config = motor_config
        self.current_id = 1
        

        if self.port_handler.openPort():
            print("Succeeded to open the port")
        else:
            print("Failed to open the port")
            self.initialized = False
            return

        if self.port_handler.setBaudRate(baudrate):
            print("Succeeded to change the baudrate")
        else:
            print("Fauled to change the baudrate")
            self.initialized = False
            return

        
        print "Initialized success!!"

        



    def set_operating_mode(self, mode):
        if not self.initialized: return

        
        dxl_comm_result, dxl_error = \
            self.packet_handler.write1ByteTxRx(self.port_handler, self.current_id, self.motor_config.ADDRESS_OPERATING_MODE, mode)

        self.error_check(dxl_comm_result, dxl_error)




    def velocity_limit(self):
        if not self.initialized: return

        dxl_velocity_limit, dxl_comm_result, dxl_error = \
            self.packet_handler.read4ByteTxRx(self.port_handler,  self.current_id, self.motor_config.ADDRESS_VELOCITY_LIMIT)

        self.error_check(dxl_comm_result, dxl_error)

        return dxl_velocity_limit


    # @param speed:
    #  
    def set_goal_velocity(self, speed):
        if not self.initialized: return
        
        if speed > 1.0: speed = 1.0
        if speed < -1.0: speed = -1.0
        
        speed *= self.velocity_limit()
        # print str(speed)

        dxl_comm_result, dxl_error = \
            self.packet_handler.write4ByteTxRx(self.port_handler, self.current_id, self.motor_config.ADDRESS_GOAL_VELOCITY, int(speed))

        self.error_check(dxl_comm_result, dxl_error)



    def set_torque_enable(self, enable):
        if not self.initialized: return

        dxl_comm_result, dxl_error = \
            self.packet_handler.write1ByteTxRx(self.port_handler, self.current_id, self.motor_config.ADDRESS_TORQUE_ENABLE, enable)

        self.error_check(dxl_comm_result, dxl_error)


    
    def set_led(self, sw):
        if not self.initialized: return

        #print str(self.motor_config.ADDRESS_LED)

        dxl_comm_result, dxl_error = \
            self.packet_handler.write1ByteTxRx(self.port_handler, self.current_id, self.motor_config.ADDRESS_LED, sw)

        self.error_check(dxl_comm_result, dxl_error)



    def error_check(self, dxl_comm_result, dxl_error):
        is_ok = True

        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packet_handler.getTxRxResult(dxl_comm_result))
            is_ok = False

        elif dxl_error != 0:
            print("%s" % self.packet_handler.getRxPacketError(dxl_error))
            is_ok = False

        else:
            pass
            #print("Dynamixel has been successfully connected")

        return is_ok
        
    def end(self):
        if not self.initialized: return

        self.port_handler.closePort()
    
    

    def id(self):
        if not self.initialized: return

        
        dxl_id, dxl_comm_result, dxl_error = \
            self.packet_handler.read1ByteTxRx(self.port_handler, self.current_id, self.motor_config.ADDRESS_ID)

        self.error_check(dxl_comm_result, dxl_error)

        return dxl_id

    def set_id(self, id):
        if not self.initialized: return

        dxl_comm_result, dxl_error = \
            self.packet_handler.write1ByteTxRx(self.port_handler, self.current_id, self.motor_config.ADDRESS_ID, id)

        self.error_check(dxl_comm_result, dxl_error)


        


        

    
