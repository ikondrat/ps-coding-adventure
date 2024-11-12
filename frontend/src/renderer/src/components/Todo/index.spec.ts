import { render, screen } from '@testing-library/svelte'
import Todo from './index.svelte'

describe('Example', () => {
  // const todoDone = { id: 1, text: 'buy milk', done: true }
  // const todoNotDone = { id: 2, text: 'do laundry', done: false }

  test('shows the todo text when rendered', () => {
    render(Todo, {
      props: {
        asd: 1
      }
    })

    expect(screen.getByText('Example')).toBeInTheDocument() // checkbox
    // expect(screen.getByText(todoDone.text)).toBeInTheDocument()
  })
})
