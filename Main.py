import datetime
import psutil
import platform
import GPUtil
import screeninfo as screeninfo
from tabulate import tabulate
from datetime import datetime
import platform
import wmi
import os
from screeninfo import get_monitors
from getmac import get_mac_address as gma
Timing = datetime.now()
import re, uuid
def LogData():
  text_file = open("File_Name.txt", "w")

  def get_size(bytes, suffix="B"):
              """
              Scale bytes to its proper format
              e.g:
                  1253656 => '1.20MB'
                  1253656678 => '1.17GB'
              """
              factor = 1024
              for unit in ["", "K", "M", "G", "T", "P"]:
                  if bytes < factor:
                      return f"{bytes:.2f}{unit}{suffix}"
                  bytes /= factor
  text_file.write("="*40+ "System Information"+ "="*30)

  uname = platform.uname()
  text_file.write(f"\nSystem: {uname.system}\n")
  text_file.write(f"Node Name: {uname.node}\n")
  text_file.write(f"Release: {uname.release}\n")
  text_file.write(f"Version: {uname.version}\n")
  text_file.write(f"Machine: {uname.machine}\n")
  text_file.write(f"Processor: {uname.processor}\n")
           # Boot Time
  text_file.write("="*40+ "Boot Time"+ "="*30)
  boot_time_timestamp = psutil.boot_time()
  bt = datetime.fromtimestamp(boot_time_timestamp)
  text_file.write(f"\nBoot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}\n")
      # let's print CPU information
  text_file.write("="*40 + "CPU Info"+ "="*30)
  c = wmi.WMI()   
  my_system = c.Win32_ComputerSystem()[0]
  text_file.write(f"\n Manufacturer: {my_system.Manufacturer}\n")
  text_file.write(f"Model: {my_system. Model}\n")
  text_file.write(f"Name: {my_system.Name}\n")
  text_file.write(f"NumberOfProcessors: {my_system.NumberOfProcessors}\n")
  text_file.write(f"SystemType: {my_system.SystemType}\n")
  text_file.write(f"SystemFamily: {my_system.SystemFamily}\n")
  info = {}
  architecture_details = platform.architecture()
  info = architecture_details
  text_file.write(f"Architectural detail: {info}\n")

  # number of cores
  text_file.write("\nPhysical cores:"+str ( psutil.cpu_count(logical=False)))
  text_file.write("\nTotal cores:"+str (psutil.cpu_count(logical=True)))
      # CPU frequencies
  cpufreq = psutil.cpu_freq()
  text_file.write(f"\nMax Frequency: {cpufreq.max:.2f}Mhz")
  text_file.write(f"\nMin Frequency: {cpufreq.min:.2f}Mhz")
  text_file.write(f"\nCurrent Frequency: {cpufreq.current:.2f}Mhz")
      # CPU usage MF~
  text_file.write("\nCPU Usage Per Core:")
  for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
           text_file.write(f"\n Core {i}: {percentage}%")
           text_file.write(f"\nTotal CPU Usage: {psutil.cpu_percent()}%\n")
           # Memory Information
  text_file.write("="*40+ "Memory Information"+ "="*40)
        #get the memory details
  svmem = psutil.virtual_memory()
  text_file.write(f"\nTotal: {get_size(svmem.total)}")
  text_file.write(f"\nAvailable: {get_size(svmem.available)}")
  text_file.write(f"\nUsed: {get_size(svmem.used)}")
  text_file.write(f"\nPercentage: {svmem.percent}% \n")
  text_file.write("="*20+ "SWAP"+ "="*20)
      # get the swap memory details (if exists)
  swap = psutil.swap_memory()
  text_file.write(f"\nTotal: {get_size(swap.total)}")
  text_file.write(f"\nFree: {get_size(swap.free)}")
  text_file.write(f"\nUsed: {get_size(swap.used)}")
  text_file.write(f"\nPercentage: {swap.percent}%\n")
      # Disk Information
  text_file.write("="*40+ "Disk Information"+ "="*40)
  text_file.write("\nPartitions and Usage:")
      # get all disk partitions
  partitions = psutil.disk_partitions()
  for partition in partitions:
              text_file.write(f"\n === Device: {partition.device} ===")
              text_file.write(f"\n  Mountpoint: {partition.mountpoint}")
              text_file.write(f"\n  File system type: {partition.fstype}")
              try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
              except PermissionError:
                  # this can be catched due to the disk that
                  # isn't ready
                  continue
  text_file.write(f"\n  Total Size: {get_size(partition_usage.total)}")
  text_file.write (f" \n Used: {get_size(partition_usage.used)}")
  text_file.write (f" \n Free: {get_size(partition_usage.free)}")
  text_file.write(f" \n Percentage: {partition_usage.percent}%\n")
          # get IO statistics since boot
  disk_io = psutil.disk_io_counters()
  text_file.write(f"\nTotal read: {get_size(disk_io.read_bytes)}")
  text_file.write(f"\nTotal write: {get_size(disk_io.write_bytes)}\n")
      # Network information
  text_file.write("="*40+ "Network Information"+ "="*40)
     # get all network interfaces (virtual and physical)
  if_addrs = psutil.net_if_addrs()
  for interface_name, interface_addresses in if_addrs.items():
              for address in interface_addresses:
                 text_file.write (f"\n=== Interface: {interface_name} ===")
                 if str(address.family) == 'AddressFamily.AF_INET':
                      text_file.write(f"\n  IP Address: {address.address}")
                      text_file.write(f"\n  Netmask: {address.netmask}")
                      text_file.write (f"\n  Broadcast IP: {address.broadcast}")
                 elif str(address.family) == 'AddressFamily.AF_PACKET':
                      text_file.write (f"\n  MAC Address: {address.address}")
                      text_file.write (f"  \n Netmask: {address.netmask}")
                      text_file.write (f" \n Broadcast MAC: {address.broadcast}\n")
           # get IO statistics since boot
  net_io = psutil.net_io_counters()
  text_file.write(f"\nTotal Bytes Sent: {get_size(net_io.bytes_sent)}")
  text_file.write(f"\nTotal Bytes Received: {get_size(net_io.bytes_recv)}\n")
  Mac_Info =gma()
  # to get the mac address of computer
  text_file.write((f"Mac Address of computer: {Mac_Info}"))
  # joins elements of getnode() after each 2 digits.
  # using regex expression
  text_file.write((f"\nThe MAC address in formatted and less complex way is : \n"))
  text_file.write((':'.join(re.findall('..', '%012x' % uuid.getnode())))+"\n")
  for monitor in get_monitors():
      width = monitor.width
      height = monitor.height

  text_file.write(f"\n Display Resolution :{str(width) + 'x' + str(height)}\n")
  text_file.write("="*40 + "GPU Details" + "="*40)
  text_file.write('\n')
  gpu_info = c.Win32_VideoController()[0]
  text_file.write(f"\nGraphics Card: {0} {gpu_info.Name}\n")
  gpus = GPUtil.getGPUs()
  list_gpus = []
  for gpu in gpus:
                          # get the GPU id
                          gpu_id = gpu.id
                          # name of GPU
                          gpu_name = gpu.name
                          # get % percentage of GPU usage of that GPU
                          gpu_load = f"{gpu.load * 100}%"
                          # get free memory in MB format
                          gpu_free_memory = f"{gpu.memoryFree}MB"
                          # get used memory
                          gpu_used_memory = f"{gpu.memoryUsed}MB"
                          # get total memory
                          gpu_total_memory = f"{gpu.memoryTotal}MB"
                          # get GPU temperature in Celsius
                          gpu_temperature = f"{gpu.temperature} °C"
                          gpu_uuid = gpu.uuid
                          list_gpus.append((
                              gpu_id, gpu_name, gpu_load, gpu_free_memory, gpu_used_memory,
                              gpu_total_memory, gpu_temperature, gpu_uuid
                          ))
  text_file.write(tabulate(list_gpus, headers=("id", "name", "load", "free memory", "used memory", "total memory","temperature", "uuid")))
  text_file.close()
if __name__ =="__main__":
           LogData()




