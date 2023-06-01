def make_input_file(
        output_path,
        atmosphere_path,
        extraterrestrial_spectrum_path,
        ozone_du,
        day_of_year,
        zenith_angle,
        rte_solver,
        mc_spherical,
        mc_photons,
        min_wavelength,
        max_wavelength,
        umu):

    with open (output_path, 'w') as f:
        f.write(f"atmosphere_file {atmosphere_path}\n")
        f.write(f"source solar {extraterrestrial_spectrum_path}\n")
        f.write(f"mol_modify O3 {ozone_du}. DU\n")
        f.write(f"mol_abs_param crs\n")
        f.write(f"day_of_year {day_of_year}\n")
        f.write(f"sza {zenith_angle}\n")
        f.write(f"\n")
        f.write(f"rte_solver {rte_solver}\n")
        f.write(f"mc_spherical {mc_spherical}\n")
        f.write(f"mc_photons {mc_photons}\n")
        f.write(f"\n")
        f.write(f"wavelength {min_wavelength} {max_wavelength}\n")
        f.write(f"umu {float(umu)}\n")
        f.write(f"\n")
        f.write(f"quiet")


# make_input_file(
#     output_path='/home/seanr/libRadtran-2.0.4/examples/test.inp',
#     atmosphere_path='/home/seanr/libRadtran-2.0.4/data/atmmod/afglus.dat',
#     extraterrestrial_spectrum_path='/home/seanr/libRadtran-2.0.4/data/solar_flux/lunar_irrad180',
#     ozone_du=300,
#     day_of_year=1,
#     zenith_angle=85,
#     rte_solver='mystic',
#     mc_spherical='1D',
#     mc_photons=100000,
#     min_wavelength=300,
#     max_wavelength=700,
#     umu=-1.0
#     )
