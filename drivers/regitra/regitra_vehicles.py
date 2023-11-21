from drivers.driver import Driver
import pandas as pd


class RegitraVehicles(Driver):
    urls = ['https://www.regitra.lt/atvduom/Atviri_TP_parko_duomenys.zip', ]
    file_names = ['Atviri_TP_parko_duomenys.csv', ]
    columns_mapping = {'marke': 'brand', 'komercinis_pav': 'commercial_name', 'gamintojo_pav': 'manufacturer_name',
                       'gamintojo_pav_baz': 'manufacturer_base_name', 'tipas': 'type', 'variantas': 'variant',
                       'versija': 'version', 'es_tipo_patvirtinimo_nr': 'es_type_approval_number',
                       'nac_tipo_patvirtinimo_nr': 'nac_type_approval_number',
                       'individual_patvirtinimo_nr': 'individual_approval_number', 'interpoliacija': 'interpolation',
                       'uzbaigtumo_pakopa': 'completion_stage', 'vairas_desineje': 'right_steering_wheel',
                       'kategorija_pilnai': 'full_category', 'kategorija_klase': 'class_category',
                       'keb_kodas': 'keb_code', 'keb_pavadinimas': 'keb_name', 'spec_kodas': 'spec_code',
                       'spec_pavadinimas': 'spec_name', 'keb_kodas_es': 'keb_code_es', 'nuosava_mase': 'own_mass',
                       'nuosava_mase_baz': 'base_own_mass', 'maks_mase': 'max_mass', 'maks_mase_f2': 'max_mass_f2',
                       'maks_mase_f5': 'max_mass_f5', 'bandomoji_mase': 'test_mass',
                       'darbinis_turis': 'operating_volume', 'galia': 'power', 'sukiu_sk': 'gear_count',
                       'galia_elektr': 'power_electric', 'degalai': 'fuels', 'degalu_rezimas': 'fuel_mode',
                       'elektrine_tp': 'electric_tp', 'hibridines_tp_kategorija': 'hybrid_tp_category',
                       'pavaru_dezes_tipas': 'transmission_type', 'co2_kiekis': 'co2_emission',
                       'co2_kiekis_wltp': 'co2_emission_wltp', 'eko_naujoves_kodas': 'eco_novelty_code',
                       'co2_sumazejimas_nedc': 'co2_reduction_nedc', 'co2_sumazejimas_wltp': 'co2_reduction_wltp',
                       'elektr_energ_sanaud_nedc': 'electric_energy_consumption_nedc',
                       'elektr_energ_sanaud_wltp_e': 'electric_energy_consumption_wltp_urban',
                       'elektr_energ_sanaud_wltp_h': 'electric_energy_consumption_wltp_highway',
                       'elektrine_rida_nedc': 'electric_range_nedc',
                       'elektrine_rida_wltp_e': 'electric_range_wltp_urban',
                       'elektrine_rida_wltp_h': 'electric_range_wltp_highway', 'tersalu_lygis': 'noise_level',
                       'tersalu_norm_akto_nr': 'noise_norm_act_number', 'ratu_baze': 'wheelbase',
                       'tv_plotis1': 'width1', 'tv_plotis2': 'width2', 'spalva': 'color',
                       'galios_mases_sant': 'power_mass_ratio', 'maks_greitis': 'max_speed',
                       'sedimu_vietu_sk': 'number_of_seats', 'stovimu_vietu_sk': 'number_of_parking_spaces',
                       'gamybos_metai': 'manufacturing_year', 'modelio_metai': 'model_year', 'rida': 'mileage',
                       'pirm_reg_data': 'first_registration_date', 'pirm_reg_data_lt': 'first_registration_date_lt',
                       'galiojimo_laik': 'validity_period', 'paskutines_reg_data': 'last_registration_date',
                       'dae_statusas': 'dae_status', 'kilmes_salis': 'country_of_origin', 'vald_tipas': 'control_type',
                       'vald_gim_dat_int': 'control_birth_date_int', 'savivaldybe': 'municipality',
                       'apskritis': 'region'}

    table_name = 'stg_lt_vehicles'

    def __init__(self) -> None:
        super().__init__()

    def download(self, url, file_path) -> str:
        return super().download(url=url, file_path=file_path)

    def load(self, file_path, separator=',') -> pd.DataFrame:
        return super().load(file_path=file_path, separator=',')

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df = super().transform(df=df)

        df = df.rename(columns=self.columns_mapping)

        return df

    def pre_execute(self):
        return super().pre_execute()

    def post_execute(self):
        with self.engine.begin() as connection:
            connection.execute('alter table `%s` add index `%s` (`%s`)' % (self.table_name,
                                                                           'idx_' + self.table_name + '_keb_kodas',
                                                                           'keb_kodas'))

    def store(self, df: pd.DataFrame) -> bool:
        df = super().store(df=df)

        return df
