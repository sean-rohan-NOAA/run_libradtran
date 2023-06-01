from multiprocessing import Process
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
lza_vec = list(range(0,181))
day_of_year = list(range(1,366))
phase = list(range(0,181))

def run_lunar_simulation(phase):
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

            for zz in sza_vec:

                print(f"Day: {dd}, LZA: {zz}, Phase: {pp}")

                make_input_file(
                    inp_file_path='/home/seanr/libRadtran-2.0.4/analysis/lza_parameters.inp',
                    atmosphere_path='/home/seanr/libRadtran-2.0.4/data/atmmod/afglus.dat',
                    extraterrestrial_spectrum_path=f"/home/seanr/libRadtran-2.0.4/data/lunar_flux/lunar_irrad{pp}",
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
                    input_path='/home/seanr/libRadtran-2.0.4/analysis/lza_parameters.inp',
                    output_path=f"/home/seanr/libRadtran-2.0.4/output/moon/moon_{dd}_{zz}_{pp}.out"
                )


# for value in phase:
#     print(value)

if __name__ == '__main__':
    phase = list(range(0,181))
    processes = []

    num_processes = 6  # Specify the number of processes to use

    # Split the input array into equal-sized chunks for each process
    chunk_size = len(phase) // num_processes
    print(chunk_size)
    for i in range(num_processes):
        start_index = i * chunk_size
        end_index = (i + 1) * chunk_size if i < num_processes - 1 else len(phase)
        chunk = phase[start_index:end_index]

        p = Process(target=run_lunar_simulation, args=(chunk,))
        processes.append(p)
        p.start()


