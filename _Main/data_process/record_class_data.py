class DataBasic():
    def __init__(self) -> None:
        pass


class DataStatic(DataBasic):
    def __init__(self):
        super().__init__()
        self.file_loc_dict = {
            'main table': {
                'category': 'FormRoute',
                'name': 'FiltedForm'
            },
            'data folder': {
                'category': 'SampleDataRoute',
                'name': 'FiltedData'
            },
            'save_form': {
                'category': 'ResultRoute',
                'name': 'FormFolder_new'
            }
        }

        self.time_col = ['Resp_t', 'end_time', 'Heart_t', 'endo_t', 'SBT_time']

        self.table_col_map = {
            'record time': 'Resp_t',
            'record ID': 'Resp_id',
            'zdt name': 'zdt_1',
            'zpx name': 'zpx_1',
        }

        self.output_name_map = {
            'machine name': 'machineType',
            'sample rate': 'RefSampleRate',
            'para data index': 'uiDataIndex',
            'vent type list': 'st_VENT_TYPE',
            'vent mode list': 'st_VENT_MODE',
            'mand type list': 'st_MAND_TYPE',
            'start index': 0
        }

        self.result_name_map = {
            'machine type': 'machine',
            'vent m bin': 'vent_m_0',
            'vent m mid': 'vent_m_1',
            'vent m end': 'vent_m_2',
            'vent still time': 'vent_t'
        }

        self.save_table_name = {
            'table result': 'record_check',
        }


class RecordObj(DataBasic):
    def __init__(self):
        super().__init__()
        self.__row = 0
        self.__time = ''
        self.__rid = ''
        self.__zdt = ''
        self.__zpx = ''
        self.__zif_loc = ''
        self.__zdt_loc = ''
        self.__zpx_loc = ''
        self.__machine = ''
        self.__sample_rate = ''
        self.__start_ind = []
        self.__para_ind = []  # keep np array
        self.__vent_type = []
        self.__vent_mode = []
        self.__mand_type = []
        self.__still_time = 0
        self.__v_m_list = []

    # use the hastter to judge if there any attri
    @property
    def row(self):
        return self.__row

    @row.setter
    def row(self, v):
        self.__row = v

    @property
    def time(self):
        return self.__time

    @time.setter
    def time(self, v):
        self.__time = v

    @time.deleter
    def time(self):
        del self.__time

    @property
    def rid(self):
        return self.__rid

    @rid.setter
    def rid(self, v):
        self.__rid = v

    @rid.deleter
    def rid(self):
        del self.__rid

    @property
    def zdt(self):
        return self.__zdt

    @zdt.setter
    def zdt(self, v):
        self.__zdt = v

    @zdt.deleter
    def zdt(self):
        del self.__zdt

    @property
    def zpx(self):
        return self.__zpx

    @zpx.setter
    def zpx(self, v):
        self.__zpx = v

    @zpx.deleter
    def zpx(self):
        del self.__zpx

    @property
    def zif_loc(self):
        return self.__zif_loc

    @zif_loc.setter
    def zif_loc(self, v):
        self.__zif_loc = v

    @property
    def zdt_loc(self):
        return self.__zdt_loc

    @zdt_loc.setter
    def zdt_loc(self, v):
        self.__zdt_loc = v

    @property
    def zpx_loc(self):
        return self.__zpx_loc

    @zpx_loc.setter
    def zpx_loc(self, v):
        self.__zpx_loc = v

    @property
    def machine(self):
        return self.__machine

    @machine.setter
    def machine(self, v):
        self.__machine = v

    @property
    def sample_rate(self):
        return self.__sample_rate

    @sample_rate.setter
    def sample_rate(self, v):
        self.__sample_rate = v

    @property
    def start_ind(self):
        return self.__start_ind

    @start_ind.setter
    def start_ind(self, list_):
        self.__start_ind = list_

    @start_ind.deleter
    def start_ind(self):
        del self.__start_ind

    @property
    def para_ind(self):
        return self.__para_ind

    @para_ind.setter
    def para_ind(self, list_):
        self.__para_ind = list_

    @para_ind.deleter
    def para_ind(self):
        del self.__para_ind

    @property
    def vent_type(self):
        return self.__vent_type

    @vent_type.setter
    def vent_type(self, list_):
        self.__vent_type = list_

    @vent_type.deleter
    def vent_type(self):
        del self.__vent_type

    @property
    def vent_mode(self):
        return self.__vent_mode

    @vent_mode.setter
    def vent_mode(self, list_):
        self.__vent_mode = list_

    @vent_mode.deleter
    def vent_mode(self):
        del self.__vent_mode

    @property
    def mand_type(self):
        return self.__mand_type

    @mand_type.setter
    def mand_type(self, list_):
        self.__mand_type = list_

    @mand_type.deleter
    def mand_type(self):
        del self.__mand_type

    @property
    def still_time(self):
        return self.__still_time

    @still_time.setter
    def still_time(self, v):
        self.__still_time = v

    @property
    def v_m_list(self):
        return self.__v_m_list

    @v_m_list.setter
    def v_m_list(self, list_):
        self.__v_m_list = list_


class DataDynamic(DataBasic):
    def __init__(self):
        super().__init__()
        self.__df = None
        self.__save_loc = ''
        self.__obj_list = []

    @property
    def df(self):
        return self.__df

    @df.setter
    def df(self, df):
        self.__df = df

    @property
    def save_loc(self):
        return self.__save_loc

    @save_loc.setter
    def save_loc(self, v):
        self.__save_loc = v

    @property
    def obj_list(self):
        return self.__obj_list

    @obj_list.setter
    def obj_list(self, list_):
        self.__obj_list = list_