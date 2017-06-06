# Copyright 2017 PyFlowGo development team (Oryaelle Magdalena Chevrel and Jeremie Labroquere)
#
# This file is part of the PyFlowGo library.
#
# The PyFlowGo library is free software: you can redistribute it and/or modify
# it under the terms of the the GNU Lesser General Public License as published by 
# the Free Software Foundation; either version 3 of the License, or 
# (at your option) any later version.
#
# The PyFlowGo library is distributed in the hope that it will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
# GNU General Public License for more details.
#
# You should have received copies of the GNU Lesser General Public License 
# along with the PyFlowGo library.  If not, see https://www.gnu.org/licenses/.

import pyflowgo.flowgo_integrator
import pyflowgo.flowgo_heat_budget
import pyflowgo.flowgo_state
import pyflowgo.flowgo_terrain_condition
import pyflowgo.flowgo_yield_strength_model_basic
import pyflowgo.flowgo_yield_strength_model_dragoni
import pyflowgo.flowgo_melt_viscosity_model_basic
import pyflowgo.flowgo_melt_viscosity_model_shaw
#import pyflowgo.flowgo_melt_viscosity_model_grd
import pyflowgo.flowgo_melt_viscosity_model_vft
import pyflowgo.flowgo_relative_viscosity_model_er
import pyflowgo.flowgo_relative_viscosity_model_kd
import pyflowgo.flowgo_relative_viscosity_model_mp
#import pyflowgo.flowgo_relative_viscosity_model_costa
import pyflowgo.flowgo_relative_viscosity_model_costa1
import pyflowgo.flowgo_relative_viscosity_model_costa2
import pyflowgo.flowgo_relative_viscosity_model_ptp1
import pyflowgo.flowgo_relative_viscosity_model_ptp2
import pyflowgo.flowgo_relative_viscosity_model_ptp3
import pyflowgo.flowgo_material_lava
import pyflowgo.flowgo_material_air
import pyflowgo.flowgo_crystallization_rate_model_basic
import pyflowgo.flowgo_crystallization_rate_model_bimodal
import pyflowgo.flowgo_crystallization_rate_model_bimodal_f_temp
# import pyflowgo.flowgo_crystallization_rate_model_from_pymelts
import pyflowgo.flowgo_crystallization_rate_model_melts
import pyflowgo.flowgo_flux_radiation_heat
import pyflowgo.flowgo_flux_forced_convection_heat
import pyflowgo.flowgo_flux_viscous_heating
import pyflowgo.flowgo_flux_heat_loss_rain
import pyflowgo.flowgo_flux_conduction_heat
import pyflowgo.flowgo_crust_temperature_model_hon
import pyflowgo.flowgo_crust_temperature_model_constant
import pyflowgo.flowgo_crust_temperature_model_bimodal
#import pyflowgo.flowgo_crust_temperature_model_hr2001
import pyflowgo.flowgo_effective_cover_crust_model_basic
import pyflowgo.flowgo_effective_cover_crust_model_bimodal
import pyflowgo.flowgo_vesicle_fraction_model_constant
import pyflowgo.flowgo_vesicle_fraction_model_bimodal
import json

import pyflowgo.base.flowgo_base_crystallization_rate_model
import pyflowgo.base.flowgo_base_melt_viscosity_model
import pyflowgo.base.flowgo_base_relative_viscosity_model
import pyflowgo.base.flowgo_base_vesicle_fraction_model
import pyflowgo.base.flowgo_base_yield_strength_model
import pyflowgo.base.flowgo_base_effective_cover_crust_model
import pyflowgo.base.flowgo_base_crust_temperature_model

class FlowgoModelFactory:
    def __init__(self, configuration_file, terrain_condition):
        self._crystallization_rate_model = ""
        self._viscosity_model = ""
        self._yield_strength_model = ""
        self._crust_temperature_model = ""

        self._effective_cover_crust_model = ""
        self._vesicle_fraction_model = ""

        self._activate_heat_budget_radiation = ""
        self._activate_heat_budget_conduction = ""
        self._activate_heat_budget_convection = ""
        self._activate_heat_budget_rain = ""
        self._activate_heat_budget_viscous_heating = ""

        self._read_initial_condition_from_json_file(configuration_file)

        # =========================
        # Crystallization rate
        # =========================
        if self._crystallization_rate_model == "basic":
            self._crystallization_rate_model_object = pyflowgo.flowgo_crystallization_rate_model_basic. \
                FlowGoCrystallizationRateModelBasic()
        elif self._crystallization_rate_model == "bimodal":
            self._crystallization_rate_model_object = pyflowgo.flowgo_crystallization_rate_model_bimodal.\
                FlowGoCrystallizationRateModelBimodal()
        elif self._crystallization_rate_model == "bimodal_f_temp":
            self._crystallization_rate_model_object = pyflowgo.flowgo_crystallization_rate_model_bimodal_f_temp.\
                FlowGoCrystallizationRateModelBimodalFonctionTemperature()
        # elif self._crystallization_rate_model == "pymelts":
        #     self._crystallization_rate_model_object = pyflowgo.flowgo_crystallization_rate_model_from_pymelts.\
        #         FlowGoCrystallizationRateModelFromPyMELTS()
        elif self._crystallization_rate_model == "melts":
            self._crystallization_rate_model_object = pyflowgo.flowgo_crystallization_rate_model_melts.\
                FlowGoCrystallizationRateModelMelts()
        else:
            raise NameError('Crystallization rate model must be "basic" or "bimodal" '
                            'or"bimodal_f_temp" or "melts" ... ')

        assert isinstance(self._crystallization_rate_model_object,
                          pyflowgo.base.flowgo_base_crystallization_rate_model.FlowGoBaseCrystallizationRateModel)

        self._crystallization_rate_model_object.read_initial_condition_from_json_file(configuration_file)

        # =========================
        # Material air
        # =========================
        self._material_air = pyflowgo.flowgo_material_air.FlowGoMaterialAir()
        self._material_air.read_initial_condition_from_json_file(configuration_file)

        # =========================
        # Vesicle fraction model
        # =========================
        if self._vesicle_fraction_model == "constant":
            self._vesicle_fraction_model_object = pyflowgo.flowgo_vesicle_fraction_model_constant. \
                FlowGoVesicleFractionModelConstant()
        elif self._vesicle_fraction_model == "bimodal":
            self._vesicle_fraction_model_object = pyflowgo.flowgo_vesicle_fraction_model_bimodal. \
                FlowGoVesicleFractionModelBimodal()
        else:
            raise NameError('vesicle fraction model must be "constant" or "bimodal" or ... ')

        assert isinstance(self._vesicle_fraction_model_object,
                          pyflowgo.base.flowgo_base_vesicle_fraction_model.FlowGoBaseVesicleFractionModel)

        self._vesicle_fraction_model_object.read_initial_condition_from_json_file(configuration_file)

        # =========================
        # Viscosity models
        # =========================

        # -------------------------
        # Melt viscosity models
        # -------------------------
        if self._melt_viscosity_model == "basic":
            self._melt_viscosity_model_object = pyflowgo.flowgo_melt_viscosity_model_basic.FlowGoMeltViscosityModelBasic()
        elif self._melt_viscosity_model == "shaw":
            self._melt_viscosity_model_object = pyflowgo.flowgo_melt_viscosity_model_shaw.FlowGoMeltViscosityModelShaw()
        #elif self._melt_viscosity_model == "grd":
            #self._melt_viscosity_model_object = pyflowgo.flowgo_melt_viscosity_model_grd.FlowGoMeltViscosityModelGRD()
        elif self._melt_viscosity_model == "vft":
            self._melt_viscosity_model_object = pyflowgo.flowgo_melt_viscosity_model_vft.FlowGoMeltViscosityModelVFT()
        else:
            raise NameError('Melt viscosity model must be "basic" or "shaw" or "vft"... ')

        assert isinstance(self._melt_viscosity_model_object,
                          pyflowgo.base.flowgo_base_melt_viscosity_model.FlowGoBaseMeltViscosityModel)

        self._melt_viscosity_model_object.read_initial_condition_from_json_file(configuration_file)

        # -------------------------
        # Relative viscosity models
        # -------------------------
        if self._relative_viscosity_model == "er":
            self._relative_viscosity_model_object = pyflowgo.flowgo_relative_viscosity_model_er.\
                FlowGoRelativeViscosityModelER()
        elif self._relative_viscosity_model == "kd":
            self._relative_viscosity_model_object = pyflowgo.flowgo_relative_viscosity_model_kd.\
                FlowGoRelativeViscosityModelKD()
        elif self._relative_viscosity_model == "mp":
            self._relative_viscosity_model_object = pyflowgo.flowgo_relative_viscosity_model_mp.\
                FlowGoRelativeViscosityModelMP()
        elif self._relative_viscosity_model == "ptp1":
            self._relative_viscosity_model_object = pyflowgo.flowgo_relative_viscosity_model_ptp1.\
                FlowGoRelativeViscosityModelPhanThienPham1(vesicle_fraction_model=self._vesicle_fraction_model_object)
        elif self._relative_viscosity_model == "ptp2":
            self._relative_viscosity_model_object = pyflowgo.flowgo_relative_viscosity_model_ptp2.\
                FlowGoRelativeViscosityModelPhanThienPham2(vesicle_fraction_model=self._vesicle_fraction_model_object)
        elif self._relative_viscosity_model == "ptp3":
            self._relative_viscosity_model_object = pyflowgo.flowgo_relative_viscosity_model_ptp3.\
                FlowGoRelativeViscosityModelPhanThienPham3(vesicle_fraction_model=self._vesicle_fraction_model_object)
        #elif self._relative_viscosity_model == "costa":
            #self._relative_viscosity_model_object = pyflowgo.flowgo_relative_viscosity_model_costa.\
                #FlowGoRelativeViscosityModelCosta()
        elif self._relative_viscosity_model == "costa1":
            self._relative_viscosity_model_object = pyflowgo.flowgo_relative_viscosity_model_costa1.\
                FlowGoRelativeViscosityModelCosta1()
        elif self._relative_viscosity_model == "costa2":
            self._relative_viscosity_model_object = pyflowgo.flowgo_relative_viscosity_model_costa2.\
                FlowGoRelativeViscosityModelCosta2()
        else:
            raise NameError('Relative viscosity model must be "er" or "kd" or "mp" or "costa1" ou "costa2" or "ptp1" or'
                            '"ptp2" or "ptp3"... ')

        assert isinstance(self._relative_viscosity_model_object,
                          pyflowgo.base.flowgo_base_relative_viscosity_model.FlowGoBaseRelativeViscosityModel)

        self._relative_viscosity_model_object.read_initial_condition_from_json_file(configuration_file)

        # -------------------------
        # Yield strength model
        # -------------------------
        if self._yield_strength_model == "basic":
            self._yield_strength_model_object = pyflowgo.flowgo_yield_strength_model_basic.FlowGoYieldStrengthModelBasic()
        elif self._yield_strength_model == "dragoni":
            self._yield_strength_model_object = pyflowgo.flowgo_yield_strength_model_dragoni.FlowGoYieldStrengthModelDragoni()
        else:
            raise NameError('Yield strength model must be "basic" or "dragoni" or ... ')

        assert isinstance(self._yield_strength_model_object,
                          pyflowgo.base.flowgo_base_yield_strength_model.FlowGoBaseYieldStrengthModel)

        self._yield_strength_model_object.read_initial_condition_from_json_file(configuration_file)

        # =========================
        # MATERIAL LAVA
        # =========================
        self._material_lava = pyflowgo.flowgo_material_lava.FlowGoMaterialLava(
            melt_viscosity_model=self._melt_viscosity_model_object,
            relative_viscosity_model=self._relative_viscosity_model_object,
            yield_strength_model=self._yield_strength_model_object,
            vesicle_fraction_model=self._vesicle_fraction_model_object)

        self._material_lava.read_initial_condition_from_json_file(configuration_file)

        # -------------------------
        # EFFECTIVE CRUST COVER MODEL
        # -------------------------
        if self._effective_cover_crust_model == "basic":
            self._effective_cover_crust_model_object = pyflowgo.flowgo_effective_cover_crust_model_basic.\
                FlowGoEffectiveCoverCrustModelBasic(terrain_condition, self._material_lava)
        elif self._effective_cover_crust_model == "bimodal":
            self._effective_cover_crust_model_object = pyflowgo.flowgo_effective_cover_crust_model_bimodal.\
                FlowGoEffectiveCoverCrustModelBimodal(terrain_condition, self._material_lava)
        else:
            raise NameError('Crust Cover model must be "basic" or "bimodal"... ')

        assert isinstance(self._effective_cover_crust_model_object,
                          pyflowgo.base.flowgo_base_effective_cover_crust_model.FlowGoBaseEffectiveCoverCrustModel)

        self._effective_cover_crust_model_object.read_initial_condition_from_json_file(configuration_file)

        # -------------------------
        # Crust temperature model
        # -------------------------
        if self._crust_temperature_model == "constant":
            self._crust_temperature_model_object = pyflowgo.flowgo_crust_temperature_model_constant.\
                FlowGoCrustTemperatureModelConstant()
        elif self._crust_temperature_model == "hon":
            self._crust_temperature_model_object = pyflowgo.flowgo_crust_temperature_model_hon.\
                FlowGoCrustTemperatureModelHon()
        elif self._crust_temperature_model == "bimodal":
            self._crust_temperature_model_object = pyflowgo.flowgo_crust_temperature_model_bimodal.\
                FlowGoCrustTemperatureModelHonBimodal()
        #elif self._crust_temperature_model == "hr2001":
           # self._crust_temperature_model_object = pyflowgo.flowgo_crust_temperature_model_hr2001.\
                #FlowGoCrustTemperatureModelHR2001()
        else:
            raise NameError('Crust temperature model must be "constant" or "hon" or "binodal" .. ')

        assert isinstance(self._crust_temperature_model_object,
                          pyflowgo.base.flowgo_base_crust_temperature_model.FlowGoBaseCrustTemperatureModel)

        self._crust_temperature_model_object.read_initial_condition_from_json_file(configuration_file)

        # =========================
        # HEAT BUDGET MODEL
        # =========================
        self._heat_budget = pyflowgo.flowgo_heat_budget.FlowGoHeatBudget()

        if self._activate_heat_budget_radiation == "yes":
            radiation_heat_flux = pyflowgo.flowgo_flux_radiation_heat.FlowGoFluxRadiationHeat(
                terrain_condition, self._material_lava, self._crust_temperature_model_object,
                self._effective_cover_crust_model_object)
            self._heat_budget.append_flux(radiation_heat_flux)
        elif self._activate_heat_budget_radiation == "no":
            pass
        else:
            raise NameError('Radiation model must be "yes" or "no"... ')

        if self._activate_heat_budget_conduction == "yes":
            heat_conduction_flux = pyflowgo.flowgo_flux_conduction_heat.FlowGoFluxConductionHeat(self._material_lava)
            self._heat_budget.append_flux(heat_conduction_flux)
        elif self._activate_heat_budget_conduction == "no":
            pass
        else:
            raise NameError('Conduction model model must be "yes" or "no"... ')

        if self._activate_heat_budget_convection == "yes":
            forced_convection_heat_flux = pyflowgo.flowgo_flux_forced_convection_heat.FlowGoFluxForcedConvectionHeat(
                terrain_condition,
                self._material_air,
                self._material_lava,
                self._crust_temperature_model_object,
                self._effective_cover_crust_model_object)
            self._heat_budget.append_flux(forced_convection_heat_flux)
        elif self._activate_heat_budget_convection == "no":
            pass
        else:
            raise NameError('Forced convection model must be "yes" or "no"... ')

        if self._activate_heat_budget_rain == "yes":
            heat_loss_rain_flux = pyflowgo.flowgo_flux_heat_loss_rain.FlowGoFluxHeatLossRain()
            self._heat_budget.append_flux(heat_loss_rain_flux)
        elif self._activate_heat_budget_rain == "no":
            pass
        else:
            raise NameError('Rain model must be "yes" or "no"... ')

        if self._activate_heat_budget_viscous_heating == "yes":
            viscous_heating_flux = pyflowgo.flowgo_flux_viscous_heating.FlowGoFluxViscousHeating(terrain_condition,
                                                                                                 self._material_lava)
            self._heat_budget.append_flux(viscous_heating_flux)
        elif self._activate_heat_budget_viscous_heating == "no":
            pass
        else:
            raise NameError('Viscous heating model must be "yes" or "no"... ')

        self._heat_budget.read_initial_condition_from_json_file(configuration_file)

    def get_effective_cover_crust_model(self):
        return self._effective_cover_crust_model_object

    def get_crust_temperature_model(self):
        return self._crust_temperature_model_object

    def get_crystallization_rate_model(self):
        return self._crystallization_rate_model_object

    def get_material_air(self):
        return self._material_air

    def get_material_lava(self):
        return self._material_lava

    def get_heat_budget(self):
        return self._heat_budget

    def _read_initial_condition_from_json_file(self, filename):
        # read json parameters file
        with open(filename) as data_file:
            data = json.load(data_file)
            self._crystallization_rate_model = data['models']['crystallization_rate_model']
            self._melt_viscosity_model = data['models']['melt_viscosity_model']
            self._relative_viscosity_model = data['models']['relative_viscosity_model']
            self._yield_strength_model = data['models']['yield_strength_model']
            self._crust_temperature_model = data['models']['crust_temperature_model']
            self._effective_cover_crust_model = data['models']['effective_cover_crust_model']
            self._vesicle_fraction_model = data['models']['vesicle_fraction_model']

            self._activate_heat_budget_radiation = data['heat_budget_models']['radiation']
            self._activate_heat_budget_conduction = data['heat_budget_models']['conduction']
            self._activate_heat_budget_convection = data['heat_budget_models']['convection']
            self._activate_heat_budget_rain = data['heat_budget_models']['rain']
            self._activate_heat_budget_viscous_heating = data['heat_budget_models']['viscous_heating']
