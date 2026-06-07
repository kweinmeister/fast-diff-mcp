// src/lib.rs
use pyo3::prelude::*;
use similar::TextDiff;

/// Compares two multiline strings and returns the difference in the
/// standard unified diff format. This is a high-performance implementation
/// written in Rust.
#[pyfunction]
fn unified_diff(text1: &str, text2: &str) -> PyResult<String> {
    let diff: TextDiff<'_, '_, str> = TextDiff::from_lines(text1, text2);
    let diff_output: String = diff
        .unified_diff()
        .header("original", "modified")
        .to_string();
    Ok(diff_output)
}

#[pymodule]
fn fast_diff_mcp(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(unified_diff, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn it_works() {
        let result: String = unified_diff("a\nb\n", "a\nc\n").unwrap();
        assert_eq!(
            result,
            "--- original\n+++ modified\n@@ -1,2 +1,2 @@\n a\n-b\n+c\n"
        );
    }
}
