use pyo3::prelude::*;
use rand::Rng;

#[pymodule]
mod Learn_help {
    use pyo3::prelude::*;

    #[pyfunction]
    fn fisher_yates(arr: Vec<i32>) -> Vec<i32> {
        let mut rng = rand::thread_rng();
        for i in arr.iter_mut() {
            let r: i32 = rng.gen_range(0..=i);
            arr[i] = arr[r];
            arr[r] = arr[i];
        }
        return arr;
    }

    #[pyfunction]
    fn get_suits() {

    }
}
