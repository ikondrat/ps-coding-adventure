import { TodoState } from './types'

export const handleEnter =
  (enterCallbackFn) =>
  (event): void => {
    if (event.key === 'Enter') {
      enterCallbackFn()
    }
  }

// Define valid transitions for each state
const VALID_TRANSITIONS: Record<TodoState, TodoState[]> = {
  [TodoState.TODO]: [TodoState.ONGOING],
  [TodoState.ONGOING]: [TodoState.DONE, TodoState.TODO],
  [TodoState.DONE]: [TodoState.ONGOING]
}

// Define the validation function for state transitions
export function isValidTransition(currentState: TodoState, newState: TodoState): boolean {
  const validNextStates = VALID_TRANSITIONS[currentState]
  return validNextStates.includes(newState)
}
