export const handleEnter =
  (enterCallbackFn) =>
  (event): void => {
    if (event.key === 'Enter') {
      enterCallbackFn()
    }
  }
