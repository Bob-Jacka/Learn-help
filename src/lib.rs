use pyo3::prelude::*;
use rand::Rng;
use std::collections::HashMap;
use pyo3::types::PyList;

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
            Self {
                question,
                answer,
                priority,
            }
        }

        fn __repr__(&self) -> String {
            format!(
                "Question: {}, Answer: {}, Priority: {}",
                self.question, self.answer, self.priority
            )
        }

        fn __getitem__(&self, prop: &str) -> PyResult<String> {
                  match prop {
                      "question" => Ok(self.question.clone()),
                      "answer" => Ok(self.answer.clone()),
                      _ => Err(pyo3::exceptions::PyKeyError::new_err(format!("Unknown property: {}",prop))),
                 }
        }
    }

    // ─────────────────────────────────────────────
    // Question_with_variants
    // ─────────────────────────────────────────────
    #[pyclass]
    #[derive(Clone)]
    pub struct Question_with_variants {
        #[pyo3(get, set)]
        pub answer: String,

        #[pyo3(get, set)]
        pub question: String,

        #[pyo3(get, set)]
        pub priority: String,

        #[pyo3(get, set)]
        pub variants: HashMap<i32, String>,
    }

    #[pymethods]
    impl Question_with_variants {
        #[new]
        #[pyo3(signature = (answer, question, priority, variants))]
        fn new(
            answer: String,
            question: String,
            priority: String,
            variants: HashMap<i32, String>,
        ) -> Self {
            Self {
                answer,
                question,
                priority,
                variants,
            }
        }

        fn __repr__(&self) -> String {
            format!(
                "Question: {}, Answer: {}, Variants: {:?}, Priority: {}",
                self.question, self.answer, self.variants, self.priority
            )
        }

        fn __getitem__(&self, prop: &str) -> PyResult<String> {
                    match prop {
                        "question" => Ok(self.question.clone()),
                        "answer" => Ok(self.answer.clone()),
                        "priority" => Ok(self.priority.clone()),
                        "variants" => Ok(self.variants.clone()),
                        _ => Err(pyo3::exceptions::PyKeyError::new_err(format!(
                            "Unknown property: {}",
                            prop
                        ))),
                    }
        }
    }

    // ─────────────────────────────────────────────
    // Question_with_ai_check
    // ─────────────────────────────────────────────
    #[pyclass]
    #[derive(Clone)]
    pub struct Question_with_ai_check {
        #[pyo3(get, set)]
        pub question: String,

        #[pyo3(get, set)]
        pub priority: String,
    }

    #[pymethods]
    impl Question_with_ai_check {
        #[new]
        fn new(question: String, priority: String) -> Self {
            Self { priority, question }
        }

        fn __getitem__(&self, prop: &str) -> PyResult<String> {
            match prop {
                "question" => Ok(self.question.clone()),
                "priority" => Ok(self.priority.clone()),
                _ => Err(pyo3::exceptions::PyKeyError::new_err(format!(
                    "Unknown property: {}",
                    prop
                ))),
            }
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
    pub struct Question_with_timer {
        #[pyo3(get, set)]
        pub question: String,

        #[pyo3(get, set)]
        pub priority: String,

        #[pyo3(get, set)]
        pub answer: String,

        #[pyo3(get, set)]
        pub time_to_wait: i32,
    }

    #[pymethods]
    impl Question_with_timer {
        #[new]
        #[pyo3(signature = (question, priority, answer, time_to_wait=10))]
        fn new(question: String, priority: String, answer: String, time_to_wait: i32) -> Self {
            Self {
                question,
                priority,
                answer,
                time_to_wait,
            }
        }

        fn __repr__(&self) -> String {
            format!(
                "Question: {}, Answer: {}, Time: {}, Priority: {}",
                self.question, self.answer, self.time_to_wait, self.priority
            )
        }

        fn __getitem__(&self, prop: &str) -> PyResult<String> {
            match prop {
                "question" => Ok(self.question.clone()),
                "answer" => Ok(self.answer.clone()),
                "priority" => Ok(self.priority.clone()),
                "time_to_wait" => Ok(self.time_to_wait.clone()),
                _ => Err(pyo3::exceptions::PyKeyError::new_err(format!("Unknown property: {}",prop))),
            }
        }
    }

    // ─────────────────────────────────────────────
    // Task_with_writing
    // ─────────────────────────────────────────────
    #[pyclass]
    #[derive(Clone)]
    pub struct Task_with_writing {
        #[pyo3(get, set)]
        pub question: String,

        #[pyo3(get, set)]
        pub answer: String,

        #[pyo3(get, set)]
        pub priority: String,
    }

    #[pymethods]
    impl Task_with_writing {
        #[new]
        #[pyo3(signature = (question, priority, answer))]
        fn new(question: String, priority: String, answer: String) -> Self {
            Self {
                question,
                priority,
                answer,
            }
        }

        fn __repr__(&self) -> String {
            format!(
                "Question: {}, Answer: {}, Priority: {}",
                self.question, self.answer, self.priority
            )
        }

        fn __getitem__(&self, prop: &str) -> PyResult<String> {
            match prop {
                "question" => Ok(self.question.clone()),
                "answer" => Ok(self.answer.clone()),
                _ => Err(pyo3::exceptions::PyKeyError::new_err(format!("Unknown property: {}",prop))),
            }
        }
    }

    ///Randomization fisher yates algorithm
    #[pyfunction]
    fn fisher_yates<'py>(mut arr: Vec<Bound<'py, PyAny>>, py: Python<'py>) -> PyResult<Bound<'py, PyAny>> {
        let mut rng = rand::thread_rng();
        for i in (1..arr.len()).rev() {
            let j = rng.gen_range(0..=i);
            arr.swap(i, j);
        }
        let list = PyList::new(py, &arr)?;
        Ok(list.into_any())
    }

    //Create question factory
    #[pyfunction]
    fn question_factory<'py>(
        question_line: String,
        py: Python<'py>,
    ) -> PyResult<Bound<'py, PyAny>> {
        if question_line.starts_with("Question") {
            let params : Vec<&str> = question_line
                           .strip_prefix("Question(")
                           .unwrap()
                           .strip_suffix(")")
                           .unwrap()
                           .split(',')
                           .collect();
            let mut params_dict: HashMap<String, String> = HashMap::new();

            for param in params {
                let splitted: Vec<_> = param.split("=").collect();
                params_dict.insert(splitted[0].trim().to_string(), splitted[1].trim().to_string());
            }

            let question_type = params_dict.get("type").cloned().unwrap_or_default(); //FIXME May cause problem, due to empty string
            let s_question = params_dict.get("question").cloned().unwrap_or_default();
            let s_answer = params_dict.get("answer").cloned().unwrap_or_default();
            let s_priority = params_dict.get("priority").cloned().unwrap_or_default(); //FIXME May cause problem, due to empty string

            //TODO make these variables only in case of special types, ex. question with time and time_to_wait available
            //For timer question:
            let time_to_wait: i32 = params_dict
                .get("time_to_wait")
                .unwrap_or(&"0".to_string())
                .parse::<i32>()
                .unwrap();

            //For variants question:
            let variants_str = params_dict.get("variants").map(|s| s.as_str()).unwrap_or("");
            let mut variants: HashMap<i32, String> = HashMap::new();

            for pair in variants_str.split(';') {
                if pair.is_empty() {
                    continue;
                }

                let mut parts = pair.splitn(2, '=');

                let key_str = parts.next().ok_or_else(|| pyo3::exceptions::PyValueError::new_err("No key in pair"))?;
                let value_str = parts.next().ok_or_else(|| pyo3::exceptions::PyValueError::new_err("No value in pair"))?;

                let key: i32 = key_str
                    .trim()
                    .parse()
                    .map_err(|_| pyo3::exceptions::PyValueError::new_err(format!("Wrong key '{}': not a number", key_str)))?;

                let value = value_str.trim().to_string();

                variants.insert(key, value);
            }

            if params_dict.contains_key("type") {
                match question_type.as_str() {
                    "Simple" => {
                        let instance = Simple_question {
                            question: s_question.to_string(),
                            answer: s_answer.to_string(),
                            priority: s_priority.to_string(),
                        };
                        let bound = Bound::new(py, instance)?;
                        return Ok(bound.into_any());
                    }
                    "Writing" => {
                        let instance = Task_with_writing {
                            question: s_question.to_string(),
                            answer: s_answer.to_string(),
                            priority: s_priority.to_string(),
                        };
                        let bound = Bound::new(py, instance)?;
                        return Ok(bound.into_any());
                    }
                    "Variants" => {
                        let instance = Question_with_variants {
                            question: s_question.to_string(),
                            answer: s_answer.to_string(),
                            variants,
                            priority: s_priority.to_string(),
                        };
                        let bound = Bound::new(py, instance)?;
                        return Ok(bound.into_any());
                    }
                    "AI" => {
                        let instance = Question_with_ai_check {
                            question: s_question.to_string(),
                            priority: s_priority.to_string(),
                        };
                        let bound = Bound::new(py, instance)?;
                        return Ok(bound.into_any());
                    }
                    "Timer" => {
                        let instance = Question_with_timer {
                            question: s_question.to_string(),
                            answer: s_answer.to_string(),
                            time_to_wait,
                            priority: s_priority.to_string(),
                        };
                        let bound = Bound::new(py, instance)?;
                        return Ok(bound.into_any());
                    }

                    &_ => {
                        panic!("Unknown tipe for question")
                    }
                }
            } else {
                panic!("Question without a type option, not supported");
            }
        }
        println!("Using fallback simple question object");
        if question_line.contains("|") {
            let splitted_old : Vec<_> = question_line.split("|").collect();

            let question = splitted_old[0];
            let answer = splitted_old[1];
            let priority = "NO";

            let instance = Simple_question {
                 question: question.to_string(),
                 answer: answer.to_string(),
                 priority: priority.to_string(),
            };
            let bound = Bound::new(py, instance)?;
            return Ok(bound.into_any());
        } else {
            let question = question_line;
            let answer = "";
            let priority = "NO";

            let instance = Simple_question {
                question: question.to_string(),
                answer: answer.to_string(),
                priority: priority.to_string(),
                };
            let bound = Bound::new(py, instance)?;
            return Ok(bound.into_any());
        }
    }

    //Settings for transpiler
    #[pyclass]
    pub struct Settings {
        ignored_names: Vec<String>,
        ignored_dirs: Vec<String>,
    }

    //Transpiler implementation in rust
    #[pyclass]
    pub struct Transpiler {
        start_path: String,
        all_questions: HashMap<String, HashMap<String, Vec<String>>>,
    }

    #[pymethods]
    impl Transpiler {
        #[new]
        #[pyo3(signature = (start_path))]
        fn new(start_path: String) -> Self {
            Self {
                start_path,
                all_questions: HashMap::new(),
            }
        }
        //      pub fn transpile(&self) {}
        //      pub fn parse_one_question(&self) {}

        //      pub fn convert_to_old_format(&self) {}
        pub fn convert_to_new_format(&self, parameters: HashMap<String, String>) -> String {
            format!(
                "Question(type={}, answer={}, priority={})",
                parameters.get("type").unwrap_or(&"Simple".to_string()),
                parameters.get("answer").unwrap_or(&"".to_string()),
                parameters.get("priority").unwrap_or(&"NO".to_string())
            )
        }

        //Simply get data from question string line
        pub fn get_data_from_question(
            &self,
            question_line_object: &str,
        ) -> HashMap<String, String> {
            let mut to_return: HashMap<String, String> = HashMap::new();

            let splitted: Vec<&str> = question_line_object
                .strip_prefix("Question(")
                .unwrap()
                .strip_suffix(")")
                .unwrap()
                .split(',')
                .collect();
            for elem in splitted {
                let (param_name, param_value): (String, String) = elem.split_once("=").into_iter().collect(); // bug fix, only 1 split due to = sym in answer
                to_return.insert(param_name.trim().to_string(), param_value);
            }
            to_return
        }

        //Delete only value from question
        //      pub fn delete_value_data_from_question(&self, mut question_str_data: String, param_key: String) -> HashMap<String, String> {
        //      }

        //Delete value and given key from question
        //      pub fn delete_key_value_data_from_question(&self, mut question_str_data: String, param_key: String) -> HashMap<String, String> {
        //      }

        //Add new parameter to question object
        //      pub fn add_data_to_question(&self, mut question_str_data: String, new_param_key: String, new_value: String) -> HashMap<String, String> {}

        //Change parameter value to another
        //      pub fn change_parameter_to(&self, mut question_str_data: String, param_key: String, new_value: String) -> HashMap<String, String> {}
    }


           //Filter through all suits in directory
//         #[pyfunction]
//         fn get_suits() {
//
//         }

           //Transpiler's method for parsing one question
//         #[pyfunction]
//         fn transpiler_parse_one_question(question_line: str) -> String {
//
//         }
//
           //Transpiler's main method for transpiling
//         #[pyfunction]
//         fn transpiler_transpile() {
//
//         }
}

//Tests for questions
#[cfg(test)]
mod Tests_questions {}

//Run it with cargo test
#[cfg(test)]
mod Tests_transpiler {

    static transpiler: Transpiler = None;

    fn setup() {
        transpiler = Transpiler::new();
    }

    fn teardown() {
        transpiler = None;
    }

    ////////////////////////////////////////

    #[test]
    fn should_transpile_one_question() {
        setup();
        //action
        teardown();
    }

    #[test]
    fn should_get_data_from_question() {
        setup();
        let question_str_object = "Question(type=Simple, question=Какие виды тестирования есть по знанию внутренней структуры, answer=Черный белый серый ящики, priority=NO)";
        let data = transpiler.get_data_from_question(question_str_object);
        assert_eq!(data["type"], "Simple");
        assert_eq!(
            data["question"],
            "Какие виды тестирования есть по знанию внутренней структуры"
        );
        assert_eq!(data["answer"], "Черный белый серый ящики");
        assert_eq!(data["priority"], "NO");
        teardown();
    }

    #[test]
    fn should_get_data_from_question_with_empty_fields() {
        setup();
        let data = transpiler.get_data_from_question("Question(type=Simple, question=Какие виды тестирования есть по знанию внутренней структуры, answer=, priority=)");
        assert_eq!(data["type"], "Simple");
        assert_eq!(
            data["question"],
            "Какие виды тестирования есть по знанию внутренней структуры"
        );
        assert_eq!(data["answer"], "");
        assert_eq!(data["priority"], "");
        teardown();
    }

    #[test]
    fn should_convert_to_new_format_with_answer() {
        setup();
        let old_format_question = "Some question|Some priority";
        let converted = transpiler.convert_to_new_format(old_format_question);
        assert_eq!(
            converted,
            "Question(type=Simple, question=Some question, answer=Some priority, priority=NO)"
        );
        teardown();
    }

    #[test]
    fn should_convert_to_new_format_with_answer() {
        setup();
        let old_format_question = "Some question";
        let converted = transpiler.convert_to_new_format(old_format_question);
        assert_eq!(
            converted,
            "Question(type=Simple, question=Some question, answer=, priority=NO)"
        );
        teardown();
    }

    #[test]
    fn should_convert_to_old_format() {
        setup();
        let new_format_question = "Question(type=Simple, question=Какие виды тестирования есть по знанию внутренней структуры, answer=, priority=)";
        let data = transpiler.convert_to_old_format();
        assert_eq!();
        teardown();
    }

    #[test]
    fn should_change_parameter() {
        setup();
        let question = "Question(type=Simple, question=Какие виды тестирования есть по знанию внутренней структуры, answer=, priority=)";
        let data = transpiler.change_parameter_to(question, "answer", "i do not know");
        assert_eq!();
        teardown();
    }

    #[test]
    fn should_delete_key_value_data_from_question() {
        setup();
        let question = "Question(type=Simple, question=Какие виды тестирования есть по знанию внутренней структуры, answer=, priority=)";
        let data = transpiler.delete_key_value_data_from_question(question, "priority");
        assert_eq!();
        teardown();
    }

    #[test]
    fn should_delete_value_from_question() {
        setup();
        let question = "Question(type=Simple, question=Какие виды тестирования есть по знанию внутренней структуры, answer=, priority=NO)";
        let data = transpiler.delete_value_data_from_question(question, "priority");
        assert_eq!(data["priority"], "");
        teardown();
    }

    #[test]
    fn should_add_new_parameter_to_question() {
        setup();
        let question = "Question(type=Simple, question=Какие виды тестирования есть по знанию внутренней структуры, answer=)";
        let data = transpiler.add_data_to_question(question, "priority", "NO");
        assert_eq!(data["type"], "Simple");
        assert_eq!(
            data["question"],
            "Какие виды тестирования есть по знанию внутренней структуры"
        );
        assert_eq!(data["answer"], "");
        assert_eq!(data["priority"], "NO");
        teardown();
    }
}
