import subprocess


def run_uvspec(uvspec_path,
               input_path,
               output_path):

    subprocess.run([uvspec_path], stdin=open(input_path, 'r'), stdout=open(output_path, 'w'), encoding='ascii')
    # subprocess.run(f"{uvspec_path} < {input_path} > {output_path}", shell=True)

# run_uvspec(
#     uvspec_path='/home/seanr/libRadtran-2.0.4/bin/uvspec',
#     input_path='/home/seanr/libRadtran-2.0.4/examples/test.inp',
#     output_path='/home/seanr/libRadtran-2.0.4/examples/test.out'
# )