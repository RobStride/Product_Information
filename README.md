# RobStride_Product_Information_CHS

# RS00

| 固件版本号   | 更新说明                                                     |
| ------------ | ------------------------------------------------------------ |
| RS00_0.0.3.3 | 1、兼容了Canopen协议和MIT协议，通过协议切换指令即可进行切换2、电机波特率修改帧、数据保存帧以及主动上报帧数据位调整，需要特定指令触发，主动上报帧反馈类型变更为243、电机恢复了恢复出厂的功能 |
| RS00_0.0.3.4 | 1、**电机的关机后反驱保护可设置是否取消**2、电机增加错误日志 |
| RS00_0.0.3.5 | 1、**csp和运控模式下可以标零，pp模式标零会屏蔽掉**2、**增加位置偏置，如果偏置填1，则以当前零点加1为零点**3、优化了长时间高速单方向跑机位置过大变量会溢出的问题4、增加了plc错误变量5、所有参数均设为可读写 |
| RS00_0.0.3.6 | 1、修正了pdo上报时间和配置不匹配的问题2、增加零位死区3、**电机canopenid与canid保持一致** |

## 特定功能详细说明

### 电机的关机后反驱保护可设置是否取消

电机在未上电状态下如果快速转动，会感受到一定的阻尼，这是电机防止外部转速过快引起浪涌设置的保护，可以通过设置0x2023 damper为1来取消该保护

### **csp和运控模式下可以标零，pp模式标零会屏蔽掉**

老版本电机标零后电机电机期望和实际值会有一个很大的偏差，电机会马上向期望值旋转，新版本电机在CSP和运控模式下标零，电机期望会马上更新为0，这样电机不会运动，PP模式下无法标零

### 增加位置偏置，如果偏置填1，则以当前零点加1为零点

有的客户因为限位影响，无法在零点位置标零，例如，在位置为1rad的地方设置零位，然后修改0x2024 add_offset为1，则重新上电后，电机的位置1rad即为之前为1rad的位置，电机的零位在之前位置1rad逆时针旋转1rad的地方

### **电机canopenid与canid保持一致**

老版本canopenid为1，新版本如果要设置canopen的id，与私有协议下的canid保持一致

# RS01

| 固件版本号   | 更新说明                                                     |
| ------------ | ------------------------------------------------------------ |
| RS01_0.1.3.3 | 1、兼容了Canopen协议和MIT协议，通过协议切换指令即可进行切换2、电机波特率修改帧、数据保存帧以及主动上报帧数据位调整，需要特定指令触发，主动上报帧反馈类型变更为243、电机恢复了恢复出厂的功能4、优化了关节电机保护算法 |
| RS01_0.1.3.4 | **1、修复电机的运控模式下kp、kd错误系数**2、增加了plc错误变量3、所有参数均设为可读写4、优化了长时间高速单方向跑机位置过大变量会溢出的问题 |
| RS01_0.1.3.5 | 1、**csp和运控模式下可以标零，pp模式标零会屏蔽掉（同rs00）**2、**canopen节点id和canid保持一致（同rs00）**3、保护算法更智能，旋转工况可运行更长时间 |
| RS01_0.1.3.6 | 1、**新增canopen标准帧切换**2、修正了pdo上报时间和配置不匹配的问题3、优化了力矩拟合曲线，出力更精准4、**取消不必要警告位** |

## 特定功能详细说明

### 修复电机的运控模式下kp、kd错误系数

旧版本运控模式系数转换存在bug，实际执行效果为t_ref=Kd*(v_set-v_actual)*1.4167+Kp*(p_set-p_actual)*1.4167+t_ff，修复后为t_ref=Kd*(v_set-v_actual)+Kp*(p_set-p_actual)+t_ff

### **新增canopen标准帧切换**

原本电机在canopen协议下无法用标准帧进行协议切换，现增加标准帧切换的协议

### **取消不必要警告位**

有电机偶尔会触发警告，警告为之前定制参数当前已无作用，后面废弃掉

# RS02

| 固件版本号   | 更新说明                                                     |
| ------------ | ------------------------------------------------------------ |
| RS02_0.2.3.4 | 1、兼容了Canopen协议和MIT协议，通过协议切换指令即可进行切换2、电机波特率修改帧、数据保存帧以及主动上报帧数据位调整，需要特定指令触发，主动上报帧反馈类型变更为243、电机恢复了恢复出厂的功能4、优化了关节电机保护算法 |
| RS02_0.2.3.6 | **1、电机的关机后反驱保护可设置是否取消（同rs00）**2、**修复电机的运控模式下kp、kd错误系数（同rs01）** |
| RS02_0.2.3.7 | 优化了长时间高速单方向跑机位置过大变量会溢出的问题           |
| RS02_0.2.3.8 | 1、**新增canopen标准帧切换（同rs01）**2、修正了pdo上报时间和配置不匹配的问题3、优化了力矩拟合曲线，出力更精准4、**取消不必要警告位（同rs01）**5、所有参数均设为可读写6、**canopen节点id和canid保持一致（同rs00）**7、**csp和运控模式下可以标零，pp模式标零会屏蔽掉（同rs00）**8、**增加位置偏置，如果偏置填1，则以当前零点加1为零点（同rs00）**9、增加零位死区 |
| RS02_0.2.3.9 | 后续批量电机硬件取消can电阻，可通过上位机标志位0x3048can_status查看该电机是否携带can电阻，为0即为初始版本有240欧姆can电阻，为1即没有can电阻 |

# RS03

| 固件版本号                    | 更新说明                                                     |
| ----------------------------- | ------------------------------------------------------------ |
| RS03_0.3.1.3                  | 1、兼容了Canopen协议和MIT协议，通过协议切换指令即可进行切换2、电机波特率修改帧、数据保存帧以及主动上报帧数据位调整，需要特定指令触发，主动上报帧反馈类型变更为243、电机恢复了恢复出厂的功能4、重新上电后的位置精度提升，需要注意的是升级后需要重新标机械零位 |
| RS03_0.3.1.4                  | **电机的关机后反驱保护可设置是否取消（同rs00）**             |
| RS03_0.3.1.5                  | 1、修复修改zero-sta为1后位置不准确的问题2、优化了长时间高速单方向跑机位置过大变量会溢出的问题 |
| RS03_0.3.1.6                  | **1、canopen节点id和canid保持一致（同rs00）**2、增加零位死区 |
| RS03_0.3.1.7                  | 修复上位机显示某几个变量错位的问题                           |
| RS03_0.3.1.8                  | 修正了pdo上报时间和配置不匹配的问题                          |
| RS03_0.3.1.9                  | 1、**csp和运控模式下可以标零，pp模式标零会屏蔽掉（同rs00）**2、**增加位置偏置，如果偏置填1，则以当前零点加1为零点（同rs00）** |
| RS03_0.3.1.10                 | 增加了plc错误变量                                            |
| RS03_APP_V0311_V1001_20250507 | 后续电机硬件取消can电阻，可通过上位机标志位0x3041can_status查看该电机是否携带can电阻，为0即为初始版本有240欧姆can电阻，为1即没有can电阻 |

# RS04

| 固件版本号    | 更新说明                                                     |
| ------------- | ------------------------------------------------------------ |
| RS04_0.4.1.3  | 1、兼容了Canopen协议和MIT协议，通过协议切换指令即可进行切换2、电机波特率修改帧、数据保存帧以及主动上报帧数据位调整，需要特定指令触发，主动上报帧反馈类型变更为243、电机恢复了恢复出厂的功能4、重新上电后的位置精度提升，需要注意的是升级后需要重新标机械零位 |
| RS04_0.4.1.6  | **1、电机的关机后反驱保护可设置是否取消（同rs00）**2、修复修改zero-sta为1后位置不准确的问题 |
| RS04_0.4.1.7  | 1、**csp和运控模式下可以标零，pp模式标零会屏蔽掉（同rs00）**2、**增加位置偏置，如果偏置填1，则以当前零点加1为零点（同rs00）** |
| RS03_0.4.1.11 | 1、修复上位机显示某几个变量错位的问题2、增加零位死区3、修复修改zero-sta为1后位置不准确的问题4、**canopen节点id和canid保持一致（同rs00）**5、堵转过载保护精确到每一相，可显示哪一相过载6、增加了plc错误变量 |
| RS04_0.4.1.12 | 修正了pdo上报时间和配置不匹配的问题                          |

# RobStride_Product_Information_EN


# RS00


| Firmware Version | Update Description                                           |
| ---------------- | ------------------------------------------------------------ |
| 1.0.0            | Initial release.                                             |
| 1.1.             | ------------                                                 |
| RS00_0.0.3.3     | 1. Compatible with both Canopen and MIT protocols, switching between them can be achieved through protocol switch instructions. 2. The data bit adjustment for motor baud rate modification frames, data save frames, and active report frames requires specific instructions to trigger. The feedback type of the active report frame has been changed to 24. 3. The motor has restored the factory reset function. |
| RS00_0.0.3.4     | 1. The reverse drive protection after motor shutdown can be set to be enabled or disabled. 2. The motor has added error logs. |
| RS00_0.0.3.5     | 1. Zeroing is allowed in csp and motion control modes, but is disabled in pp mode. 2. Position offset has been added; if the offset is set to 1, the current zero point plus 1 will be the new zero point. 3. Optimized the issue where large position variables would overflow during long-term high-speed unidirectional operation. 4. Added PLC error variables. 5. All parameters are now set as readable and writable. |
| RS00_0.0.3.6     | 1. Fixed the issue where the PDO reporting time did not match the configuration. 2. Added a zero dead zone. 3. The motor's CANopen ID and CAN ID are now consistent. |

Detailed Description of Specific Functions 

The reverse drive protection of the motor after shutdown can be set to be cancelled or not. 

If the motor is spun rapidly when it is not powered on, a certain amount of damping can be felt. This is a protection mechanism set by the motor to prevent surges caused by excessive external rotational speed. This protection can be disabled by setting 0x2023 damper to 1. 

Zero marking is allowed in CSP and operation control modes, but it will be blocked in PP mode. 

In the old version, after zeroing the motor, there would be a significant deviation between the expected and actual values of the motor, causing it to immediately rotate towards the expected value. In the new version, when zeroing the motor in CSP and motion control modes, the expected value of the motor is immediately updated to 0, so the motor does not move. Zeroing is not possible in PP mode. 

Increase the position bias. If the bias is filled with 1, then take the current zero point plus 1 as the new zero point. 

Some customers are unable to set zero at the zero position due to limit effects. For instance, if the zero position is set at 1 radian and the 0x2024 add_offset is modified to 1, after a power cycle, the motor's position at 1 radian will be the same as the previous 1 radian position, and the motor's zero position will be 1 radian counterclockwise from the previous 1 radian position. 

The CANOPENID of the motor should be consistent with the CANID. 

For the old version, CANOPENID is 1. For the new version, if you want to set the CANOPEN ID, it should be consistent with the CANID under the private protocol. 

# RS01


| Firmware Version | Update Description                                           |
| ---------------- | ------------------------------------------------------------ |
| 1.0.0            | Initial release.                                             |
| 1.1.0            | ------------                                                 |
| RS01_0.1.3.3     | 1. Compatible with both Canopen and MIT protocols, switching between them can be achieved through protocol switching instructions. 2. The data bit adjustment for motor baud rate modification frames, data saving frames, and active reporting frames requires specific instructions to trigger. The feedback type of the active reporting frame has been changed to 24. 3. The motor has restored the factory reset function. 4. Optimized the protection algorithm for joint motors. |
| RS01_0.1.3.4     | 1. Fixed the incorrect kp and kd coefficients in the motor's operation control mode. 2. Added PLC error variables. 3. All parameters are now set as readable and writable. 4. Optimized the issue where large variables would overflow when running at high speed in a single direction for a long time. |
| RS01_0.1.3.5     | 1. Zeroing is now possible in both CSP and operation control modes, while zeroing in PP mode is disabled (same as RS00). 2. The Canopen node ID and CanID are now consistent (same as RS00). 3. The protection algorithm is more intelligent, allowing for longer operation under rotational conditions. |
| RS01_0.1.3.6     | 1. Added the ability to switch Canopen standard frames. 2. Fixed the issue where PDO reporting time did not match the configuration. 3. Optimized the torque fitting curve for more accurate output. 4. Removed unnecessary warning bits. |

Detailed Description of Specific Functions 

Fix the incorrect kp and kd coefficients in the motor's operation control mode. 

There was a bug in the coefficient conversion of the old version's operation control mode. The actual execution effect was t_ref = Kd * (v_set - v_actual) * 1.4167 + Kp * (p_set - p_actual) * 1.4167 + t_ff. After the fix, it became t_ref = Kd * (v_set - v_actual) + Kp * (p_set - p_actual) + t_ff. 

### **New CANopen Standard Frame Switching** 

Originally, the motor could not switch protocols using standard frames under the CANopen protocol. Now, a protocol for switching with standard frames has been added. 

### **Disable Unnecessary Warning Positions** 

Occasionally, some motors will trigger a warning that the previously customized parameters are no longer effective and will be discarded later. 

# RS02


| Firmware Version | Update Description                                           |
| ---------------- | ------------------------------------------------------------ |
| 1.0.0            | Initial release.                                             |
| 1.1.             | ------------                                                 |
| RS02_0.2.3.4     | 1. Compatible with both Canopen and MIT protocols, and can be switched by protocol switching instructions. 2. The data bit adjustment for motor baud rate modification frames, data saving frames, and active reporting frames requires specific instructions to trigger. The feedback type of the active reporting frame has been changed to 24. 3. The motor has regained the factory reset function. 4. Optimized the protection algorithm for joint motors. |
| RS02_0.2.3.6     | 1. The reverse drive protection after motor shutdown can be set to be cancelled or not (same as RS00). 2. Fixed the incorrect kp and kd coefficients in the motor's motion control mode (same as RS01). |
| RS02_0.2.3.7     | Optimized the issue where the position variable would overflow after long-term high-speed unidirectional operation. |
| RS02_0.2.3.8     | 1. Added Canopen standard frame switching (same as RS01). 2. Fixed the issue where the PDO reporting time did not match the configuration. 3. Optimized the torque fitting curve for more accurate output. 4. Removed unnecessary warning bits (same as RS01). 5. All parameters are now set as readable and writable. 6. The Canopen node ID and CanID are now consistent (same as RS00). 7. Zeroing is now possible in CSP and motion control modes, but is disabled in PP mode (same as RS00). 8. Added position offset. If the offset is set to 1, the current zero point plus 1 will be the new zero point (same as RS00). 9. Added a zero dead zone. |
| RS02_0.2.3.9     | For subsequent batch motors, the CAN resistor has been removed from the hardware. The presence of a CAN resistor can be checked through the upper computer flag bit 0x3048can_status. A value of 0 indicates the initial version with a 240-ohm CAN resistor, while a value of 1 indicates no CAN resistor. |

# RS03


| Firmware Version Number       | Update Description                                           |
| ----------------------------- | ------------------------------------------------------------ |
| RS03_0.3.1.3                  | 1. Compatible with both Canopen and MIT protocols. Protocol switching can be achieved through the protocol switch command. 2. The data bit adjustment for the motor baud rate modification frame, data save frame, and active report frame requires specific instructions to trigger. The feedback type of the active report frame has been changed to 24. 3. The factory reset function of the motor has been restored. 4. The position accuracy after re-powering has been improved. Please note that the mechanical zero position needs to be recalibrated after the upgrade. |
| RS03_0.3.1.4                  | The reverse drive protection after motor shutdown can be set to be enabled or disabled (same as RS00). |
| RS03_0.3.1.5                  | 1. Fixed the issue where the position was inaccurate after setting zero-sta to 1. 2. Optimized the problem where the position variable would overflow after running in a single direction at high speed for a long time. |
| RS03_0.3.1.6                  | 1. The Canopen node ID and CanID are consistent (same as RS00). 2. Added a zero dead zone. |
| RS03_0.3.1.7                  | Fixed the issue where certain variables were displayed incorrectly on the upper computer. |
| RS03_0.3.1.8                  | Fixed the issue where the PDO report time did not match the configuration. |
| RS03_0.3.1.9                  | 1. Zeroing is allowed in CSP and motion control modes, but is disabled in PP mode (same as RS00). 2. Added position offset. If the offset is set to 1, the current zero point plus 1 will be the new zero point (same as RS00). |
| RS03_0.3.1.10                 | Added PLC error variables.                                   |
| RS03_APP_V0311_V1001_20250507 | In subsequent motor hardware, the CAN resistor is removed. The presence of a CAN resistor can be checked through the upper computer flag bit 0x3041can_status. A value of 0 indicates the initial version with a 240-ohm CAN resistor, while a value of 1 indicates no CAN resistor. |

# RS04


| Firmware Version | Update Description                                           |
| ---------------- | ------------------------------------------------------------ |
| RS04_0.4.1.3     | 1. Compatible with both Canopen and MIT protocols, and can be switched by protocol switching instructions. 2. The data bit adjustment for motor baud rate modification frames, data saving frames, and active reporting frames requires specific instructions to trigger. The feedback type of the active reporting frame has been changed to 24. 3. The motor has restored the factory reset function. 4. The position accuracy after re-powering has been improved. Please note that the mechanical zero position needs to be recalibrated after the upgrade. |
| RS04_0.4.1.6     | 1. The reverse drive protection after motor shutdown can be set to be enabled or disabled (same as RS00). 2. Fixed the issue where the position was inaccurate after setting zero-sta to 1. |
| RS04_0.4.1.7     | 1. Zeroing can be performed in CSP and motion control modes, but is disabled in PP mode (same as RS00). 2. Added position offset. If the offset is set to 1, the current zero point plus 1 will be the new zero point (same as RS00). |
| RS03_0.4.1.11    | 1. Fixed the issue where certain variables were displayed out of position on the upper computer. 2. Added a zero dead zone. 3. Fixed the issue where the position was inaccurate after setting zero-sta to 1. 4. The Canopen node ID and CanID are consistent (same as RS00). 5. The stall overload protection is precise to each phase and can display which phase is overloaded. 6. Added PLC error variables. |
| RS04_0.4.1.12    | Fixed the issue where the PDO reporting time did not match the configuration. |
