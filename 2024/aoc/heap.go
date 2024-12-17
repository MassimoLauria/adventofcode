package aoc

type MinHeap[T comparable] struct {
	data  []T
	cost  []int
	index map[T]int
}

func NewMinHeap[T comparable]() *MinHeap[T] {
	var Q MinHeap[T]
	Q.data = make([]T, 0)
	Q.cost = make([]int, 0)
	Q.index = make(map[T]int)
	return &Q
}

func (q *MinHeap[T]) Len() int {
	return len(q.data)
}

func (q *MinHeap[T]) Swap(i, j int) {
	if i == j {
		return
	}
	ei, ej := q.data[i], q.data[j]
	q.index[ei] = j
	q.index[ej] = i
	q.data[i], q.data[j] = ej, ei
	q.cost[j], q.cost[i] = q.cost[i], q.cost[j]
}

func (q *MinHeap[T]) updateUp(idx int) {
	pidx := (idx - 1) / 2
	for idx > 0 && q.cost[pidx] < q.cost[idx] {
		q.Swap(pidx, idx)
		idx = pidx
		pidx = (idx - 1) / 2
	}
}

func (q *MinHeap[T]) updateDown(idx int) {
	var min_idx, lidx, ridx int
	for idx < q.Len() {
		lidx = 2*idx + 1
		ridx = 2*idx + 2
		min_idx = idx
		if lidx < q.Len() && q.cost[lidx] < q.cost[min_idx] {
			min_idx = lidx // maybe swap with left child
		}
		if ridx < q.Len() && q.cost[ridx] < q.cost[min_idx] {
			min_idx = ridx // maybe swap with right child
		}
		if min_idx != idx {
			q.Swap(min_idx, idx)
			idx = min_idx
		} else {
			break
		}
	}
}

func (q *MinHeap[T]) Pop() (T, int) {
	end := q.Len() - 1
	q.Swap(0, end)
	v, c := q.data[end], q.cost[end]
	q.data = q.data[:end]
	q.cost = q.cost[:end]
	delete(q.index, v)
	q.updateDown(0)
	return v, c
}

func (q *MinHeap[T]) Peek() (T, int) {
	return q.data[0], q.cost[0]
}

func (q *MinHeap[T]) Improve(value T, cost int) {
	idx, ok := q.index[value]
	if ok && q.cost[idx] <= cost { // no update
		return
	}

	if ok && q.cost[idx] > cost { // old element
		q.cost[idx] = cost
	} else { // new element
		q.data = append(q.data, value)
		q.cost = append(q.cost, cost)
		q.index[value] = len(q.data) - 1
		idx = len(q.data) - 1
	}
	q.updateUp(idx)
}
