from pathlib import Path, PurePath
import numpy as np
from numpy.core.defchararray import array


class RecordFucBasic():
    def __init__(self) -> None:
        pass


class FileLocBuild(RecordFucBasic):
    def __init__(self, cwd, obj_table, obj_record):
        super().__init__()
        self.__cwd = cwd
        self.__obj_1 = obj_table
        self.__obj_2 = obj_record

    def __Folder(self, main_loc, time_info, rid):
        parents_2 = Path(main_loc) if not isinstance(main_loc,
                                                     PurePath) else main_loc
        parents_1 = (str(time_info.year) + str(time_info.month).rjust(2, '0'))
        parents_0 = rid
        folder_loc = parents_2 / parents_1 / parents_0

        return folder_loc

    def ZifLoc(self):
        parent_loc = self.__Folder(self.__cwd, self.__obj_1.time,
                                   self.__obj_1.rid)
        self.__obj_2.zif_loc = parent_loc / (self.__obj_1.rid + '.zif')

    def ZdtLoc(self):
        parent_loc = self.__Folder(self.__cwd, self.__obj_1.time,
                                   self.__obj_1.rid)
        self.__obj_2.zdt_loc = parent_loc / (self.__obj_1.zdt + '.zdt')

    def ZpxLoc(self):
        parent_loc = self.__Folder(self.__cwd, self.__obj_1.time,
                                   self.__obj_1.rid)
        self.__obj_2.zpx_loc = parent_loc / (self.__obj_1.zpx + '.zpx')


class OutputCheck(RecordFucBasic):
    def __init__(self, obj):
        super().__init__()
        self.__obj = obj
        self.__size_min = 100

    def ZifContentCheck(self, func):
        default = None
        if self.__obj.zif_loc.stat().st_size >= self.__size_min:
            return func(self.__obj.zif_loc)
        else:
            return default

    def ZdtHeaderCheck(self, func):
        default = {}
        if self.__obj.zdt_loc.stat().st_size >= self.__size_min:
            return func(self.__obj.zdt_loc)[0]
        else:
            return default

    def ZdtContentCheck(self, class_):
        default = [[], [], [], [], [], 0]
        if self.__obj.zdt_loc.stat().st_size >= self.__size_min:
            return class_(self.__obj.zdt_loc)
        else:
            return default


class Calculation(RecordFucBasic):
    def __init__(self, p_start, p_end):
        super().__init__()
        self.__pro_ind = p_start
        self.__end_ind = p_end
        self.__min_ind = 0
        self.__p_in = np.array([])
        self.__p_ex = np.array([])
        self.__v_in = np.array([])
        self.__v_ex = np.array([])

        self.valid_tag = True

    def __GapDetection(self):
        min_gap = 50
        max_gap = 450
        gap = abs(self.__end_ind - self.__pro_ind)

        if gap < min_gap or gap > max_gap or gap == 0:
            return False
        else:
            return True

    def __LineDetection(self, array_):

        if np.all(array_ == array_[0]):
            return False
        else:
            return True

    def __SwitchPoint(self, array_):
        interval = 15
        ind_array = np.where(array_[interval:] < 0)[0]
        try:
            ind = ind_array[0] + interval
        except:
            ind = None
        return ind

    def __LenMatch(self, array_1, array_2):
        len_1 = array_1.shape[0]
        len_2 = array_2.shape[0]

        if len_1 != len_2:
            self.valid_tag = False

    def __ArrayCertify(self, list_):
        list_ = [list_] if type(list_) == np.array else list_

        for array in list_:
            if not np.any(array):
                self.valid_tag = False
                return

    def ValidityCheck(self, s_F, s_V, s_P):
        if self.__GapDetection():
            f_wave = np.array(s_F[self.__pro_ind:self.__end_ind])
            if self.__LineDetection(f_wave) and self.__SwitchPoint(f_wave):
                self.__min_ind = self.__SwitchPoint(f_wave) + self.__pro_ind
                if self.__min_ind != self.__pro_ind:

                    self.__p_in = np.array(s_P[self.__pro_ind:self.__min_ind])
                    self.__p_ex = np.array(s_P[self.__min_ind:self.__end_ind])
                    self.__v_in = np.array(s_V[self.__pro_ind:self.__min_ind])
                    self.__v_ex = np.array(s_V[self.__min_ind:self.__end_ind])

                    self.__ArrayCertify(
                        [self.__p_in, self.__p_ex, self.__v_in, self.__v_ex])
                    self.__LenMatch(self.__p_in, self.__v_in)
                    self.__LenMatch(self.__p_ex, self.__v_ex)

                else:
                    self.valid_tag = False
            else:
                self.valid_tag = False
        else:
            self.valid_tag = False

    def RR(self, sample_rate):
        vent_len = self.__end_ind - self.__pro_ind
        RR = 60 / (vent_len * 1 / sample_rate)
        return round(RR, 2)

    def V_t_i(self):
        v_t_i = self.__v_in[-1]
        return round(v_t_i, 2)

    def V_t_e(self):
        v_t_e = self.__v_in[-1] + (self.__v_ex[-1] if self.__v_ex[-1] < 0 else
                                   -self.__v_ex[-1])
        return round(v_t_e, 2)

    def WOB(self):
        wob_angle = (self.__p_in[-1] * self.__v_in[-1]) / 1000
        wob_a = abs(wob_angle - abs(np.trapz(self.__v_in, self.__p_in)) / 1000)
        wob_b = abs(wob_angle - abs(np.trapz(self.__v_ex, self.__p_ex)) / 1000)
        wob = wob_a + wob_b

        return round(wob, 2)

    def VE(self, rr, v_t):
        VE = rr * (v_t / 1000)
        return round(VE, 2)

    def RSBI(self, rr, v_t):
        rsbi = rr / (v_t / 1000)
        return round(rsbi, 2)


class Analysis(RecordFucBasic):
    def __init__(self):
        super().__init__()

    def Mean(self, list_):
        array_ = np.array(list_)
        result = np.mean(array_)
        return round(result, 2)

    def StanDev(self, list_):
        array_ = np.array(list_)
        result = np.std(array_)
        return round(result, 2)