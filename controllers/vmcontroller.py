import csv

class SearchVms(object):

    def get(self, requestData):
        # GET RESULTS FROM SIZE FILE
        vmsSize = self.get_bysize(requestData)
        # GET RESULTS FROM PRICE FILE
        vmsPrice = self.get_price(requestData)

        vmCompareList = []

        # MATCH RESULTS OF BOTH LISTS
        for vmp in vmsPrice:
            for vms in vmsSize:
                if vms.get('armSkuName') == vmp.get('armSkuName'):
                    vmCompareList.append({
                        'armSkuName': vmp.get('armSkuName'), 
                        'numberOfCores': vms.get('numberOfCores'),
                        'memoryInMB': vms.get('memoryInMB'),
                        'os': vmp.get('os'),
                        'unitPricePerUnit': vmp.get('unitPricePerUnit')
                        })

        # RETURN SINGLE SMALLEST VALUE
        vmResult = list(sorted(vmCompareList, key=lambda vm: vm['unitPricePerUnit']))[0]

        return vmResult

    def get_bysize(self, requestData):

        try:
            # READ CSV TO RETRIEVE SIZING DATA
            with open(r"dataset/Exam rightsizing.csv") as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=';')
                line_count = 0

                vmsFilteredSize = []

                for row in csv_reader:
                    # SKIP HEADER ROW
                    if line_count == 0:
                        line_count += 1
                        continue
                    
                    if row[0]:
                        armSkuName = row[0]
                        numberOfCores = int(row[1])
                        osDiskSizeInMB =int(row[2])
                        memoryInMB =int(row[3])
                        maxDataDiskCount =int(row[4])
                        meterName =row[5]

                        # FIND IF RECORD MATCHES FORM VALUES AND CREATE DICT
                        if numberOfCores == int(requestData.get('cores')) and memoryInMB == int(requestData.get('ram')) * 1024:
                            obj = {'armSkuName': row[0], 
                                'numberOfCores': int(row[1]),
                                'osDiskSizeInMB': int(row[2]),
                                'memoryInMB': int(row[3]),
                                'maxDataDiskCount': int(row[4]),
                                'meterName': row[5]}
                            vmsFilteredSize.append(obj)
            
            return vmsFilteredSize


        except:
            print("Error search size")
    

    def get_price(self, requestData):
        try:
            # READ CSV TO RETRIEVE SIZING DATA
            with open(r"dataset/Exam Pricesheet.csv") as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=';')
                line_count = 0

                vmsFilteredPrice = []

                for row in csv_reader:
                    # SKIP HEADER ROW
                    if line_count == 0:
                        line_count += 1
                        continue
                    
                    if row[0]:
                        armSkuName = row[1]
                        vmOs = row[19]
                        unitPricePerUnit = row[20]

                        # FIND IF RECORD MATCHES FORM VALUES AND CREATE DICT
                        if vmOs.upper() == requestData.get('os').upper():
                            obj = {
                                'armSkuName': row[1],
                                'os': row[19],
                                'unitPricePerUnit': row[20]}
                            vmsFilteredPrice.append(obj)
            
            return vmsFilteredPrice


        except:
            print("Error search price")