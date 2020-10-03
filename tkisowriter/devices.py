import subprocess
import json


# ─── USB DEVICES MANAGER CLASS ──────────────────────────────────────────────────

class DevicesInfo:
    ''' Read all output from 'lsblk' and filter usb devices '''
    
    data = None

    def refresh(self):
        ''' Read and save data from lsblk '''
        res = subprocess.check_output("lsblk -J --output-all", shell=True).decode("utf-8") 
        self.data = json.loads(res)

    @property
    def usb_list(self):
        ''' Return list of USB devices detected '''
        res = []
        if self.data is not None:
            for d in self.data['blockdevices']:
                if d['hotplug']:
                    res.append(d['path'])
        return res

    def get_info(self, device):
        ''' Search path on devices detected and return info of his device '''
        if self.data is not None:
            for d in self.data['blockdevices']:
                if d['path'] == device:
                    return d['vendor']
        return None

# ────────────────────────────────────────────────────────────────────────────────
