from multiprocessing import Process
import subprocess
import io
# import numpy as np

NCORES = 6

def run_uvspec(uvspec_path,
               input_path,
               output_path):

    process = subprocess.run([uvspec_path],
                             stdin=open(input_path, 'r'),
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             encoding='ascii')

    # arr = np.genfromtxt(io.StringIO(process.stdout))[:, [0,2]]

    # np.savetxt(output_path,
    #            arr,
    #            delimiter=' ',
    #            fmt=['%d'] + ['%.18e'] * (arr.shape[1] - 1))

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
sza_vec = list(range(0,132,1))

def run_solar_simulation(day_list):
        
    for dd in day_list:
    
        print(f"Day: {dd}")

        for zz in sza_vec:
            mc_photons = 100000
            
            if zz > 80:
                mc_photons = 200000
            
            if zz > 90:
                mc_photons = 500000
            
            if zz > 100:
                mc_photons = 1000000
            
            if zz > 110:
                mc_photons = 1500000


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
                output_path=f"/home/seanr/libRadtran-2.0.4/output/sun/sun_{dd}_{zz}.out"
                )


if __name__ == '__main__':
    day_of_year = list(range(1,366, 1))
    processes = []

    num_processes = NCORES  # Specify the number of processes to use

    # Split the input array into equal-sized chunks for each process
    chunk_size = len(day_of_year) // num_processes
    for i in range(num_processes):
        start_index = i * chunk_size
        end_index = (i + 1) * chunk_size if i < num_processes - 1 else len(day_of_year)
        chunk = day_of_year[start_index:end_index]

        p = Process(target=run_solar_simulation, args=(chunk,))
        processes.append(p)
        p.start()