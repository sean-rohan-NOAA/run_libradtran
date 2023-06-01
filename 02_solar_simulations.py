import subprocess

def run_uvspec(uvspec_path,
               input_path,
               output_path):

    process = subprocess.run([uvspec_path],
                             stdin=open(input_path, 'r'),
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             encoding='ascii')
    
    with open (output_path, 'w') as outfile:
        outfile.write(process.stdout)

def make_input_file(
        inp_file_path,
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

    with open (inp_file_path, 'w') as f:
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

# Lunar irradiance
sza_vec = list(range(0,181))
day_of_year = list(range(1,366))

for pp in phase:

    mc_photons = 50000

    if pp > 80:
        mc_photons = 100000

    if pp > 100:
        mc_photons = 200000

    for dd in day_of_year:

        print(f"Day: {dd}, Phase: {pp}, LZA: {zz}")

        for zz in sza_vec:

            make_input_file(
                inp_file_path='/home/seanr/libRadtran-2.0.4/analysis/sza_parameters.inp',
                atmosphere_path='/home/seanr/libRadtran-2.0.4/data/atmmod/afglus.dat',
                extraterrestrial_spectrum_path=f"/home/seanr/libRadtran-2.0.4/data/solar_flux/apm_1nm",
                ozone_du=300,
                day_of_year=dd,
                zenith_angle=zz,
                rte_solver='mystic',
                mc_spherical='1D',
                mc_photons=mc_photons,
                min_wavelength=300,
                max_wavelength=750,
                umu=-1.0
                )

            run_uvspec(
                uvspec_path='/home/seanr/libRadtran-2.0.4/bin/uvspec',
                input_path='/home/seanr/libRadtran-2.0.4/analysis/sza_parameters.inp',
                output_path=f"/home/seanr/libRadtran-2.0.4/output/sun/sun_{dd}_{zz}_{pp}.out"
            )

if __name__ == '__main__':
    phase = list(range(0,181))
    processes = []

    num_processes = 6  # Specify the number of processes to use

    # Split the input array into equal-sized chunks for each process
    chunk_size = len(input_array) // num_processes
    for i in range(num_processes):
        start_index = i * chunk_size
        end_index = (i + 1) * chunk_size if i < num_processes - 1 else len(input_array)
        chunk = input_array[start_index:end_index]

        p = Process(target=bubble_sort, args=(chunk,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()