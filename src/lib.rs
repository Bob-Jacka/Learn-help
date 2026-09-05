use pyo3::prelude::*;
use rand::Rng;
use std::collections::HashMap;

#[pymodule]
mod learn_help {
    use super::*;

    /*
    Simple question without unnecessary things
    */
    #[pyclass]
    #[derive(Clone)]
    struct Simple_question {

        #[pyo3(get, set)]
        pub question: String,

        #[pyo3(get, set)]
        pub answer: String,

        #[pyo3(get, set)]
        pub priority: String,
    }

    #[pymethods]
    impl Simple_question {
        #[new]
        fn new(question: String, answer: String, priority: String) -> Self {
            Simple_question { question, answer, priority }
        }
    }

    // ─────────────────────────────────────────────
    // Question_with_variants
    // ─────────────────────────────────────────────
    #[pyclass]
    #[derive(Clone)]
    pub struct QuestionWithVariants {
        #[pyo3(get)]
        pub answer: String,

        #[pyo3(get)]
        pub question: String,

        #[pyo3(get)]
        pub priority: String,

        #[pyo3(get)]
        pub variants: HashMap<i32, String>,
    }

    #[pymethods]
    impl QuestionWithVariants {
        #[new]
        #[pyo3(signature = (answer, question, priority, variants))]
        fn new(answer: String, question: String, priority: String, variants: HashMap<i32, String>) -> Self {
            Self { answer, question, priority, variants }
        }

        fn __repr__(&self) -> String {
            format!(
                "Question: {}, Answer: {}, Variants: {:?}, Priority: {}",
                self.question, self.answer, self.variants, self.priority
            )
        }
    }

    // ─────────────────────────────────────────────
    // Question_with_ai_check
    // ─────────────────────────────────────────────
    #[pyclass]
    #[derive(Clone)]
    pub struct QuestionWithAiCheck {

        #[pyo3(get)]
        pub priority: String,

        #[pyo3(get)]
        pub question: String,
    }

    #[pymethods]
    impl QuestionWithAiCheck {
        #[new]
        fn new(priority: String, question: String) -> Self {
            Self { priority, question }
        }

        fn __getitem__(&self, prop: &str) -> PyResult<String> {
            match prop {
                "question" => Ok(self.question.clone()),
                "answer" => self.get_answer(),
                _ => Err(pyo3::exceptions::PyKeyError::new_err(format!("Unknown property: {}", prop))),
            }
        }

        fn get_answer(&self) -> PyResult<String> {
            Ok(String::new())
        }

        fn __repr__(&self) -> String {
            format!(
                "Question: {}, Answer: AI generating, Priority: {}",
                self.question, self.priority
            )
        }
    }

    // ─────────────────────────────────────────────
    // Question_with_timer
    // ─────────────────────────────────────────────
    #[pyclass]
    #[derive(Clone)]
    pub struct QuestionWithTimer {
        #[pyo3(get, set)]
        pub question: String,

        #[pyo3(get, set)]
        pub priority: String,

        #[pyo3(get, set)]
        pub answer: Option<String>,

        #[pyo3(get, set)]
        pub time_to_wait: i32,
    }

    #[pymethods]
    impl QuestionWithTimer {
        #[new]
        #[pyo3(signature = (question, priority, answer=None, time_to_wait=10))]
        fn new(question: String, priority: String, answer: Option<String>, time_to_wait: i32) -> Self {
            Self { question, priority, answer, time_to_wait }
        }

        fn __repr__(&self) -> String {
            let answer_str = self.answer.as_deref().unwrap_or("None");
            format!(
                "Question: {}, Answer: {}, Time: {}, Priority: {}",
                self.question, answer_str, self.time_to_wait, self.priority
            )
        }
    }

    // ─────────────────────────────────────────────
    // Task_with_writing
    // ─────────────────────────────────────────────
    #[pyclass]
    #[derive(Clone)]
    pub struct TaskWithWriting {
        #[pyo3(get, set)]
        pub question: String,

        #[pyo3(get, set)]
        pub priority: String,

        #[pyo3(get, set)]
        pub answer: Option<String>,
    }

    #[pymethods]
    impl TaskWithWriting {
        #[new]
        #[pyo3(signature = (question, priority, answer=None))]
        fn new(question: String, priority: String, answer: Option<String>) -> Self {
            Self { question, priority, answer }
        }

        fn __repr__(&self) -> String {
            let answer_str = self.answer.as_deref().unwrap_or("None");
            format!(
                "Question: {}, Answer: {}, Priority: {}",
                self.question, answer_str, self.priority
            )
        }
    }


    //Randomization algorithm
    #[pyfunction]
    fn fisher_yates(mut arr: Vec<Simple_question>) -> Vec<Simple_question> {
        let mut rng = rand::thread_rng();
        for i in (1..arr.len()).rev() {
            let j = rng.gen_range(0..=i);
            arr.swap(i, j);
        }
        arr
    }

//
//     //Filter through all suits in directory
//     #[pyfunction]
//     fn get_suits() {
//
//     }
//
//     //Transpiler's method for parsing one question
//     #[pyfunction]
//     fn transpiler_parse_one_question(question_line: str) {
//
//     }
//
//     //Transpiler's main method for transpiling
//     #[pyfunction]
//     fn transpiler_transpile() {
//
//     }
}
