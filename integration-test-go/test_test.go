//go:build integration
// +build integration

package test

import (
	"testing"
)

func TestA(t *testing.T) {
	t.Log("Test Done:", calc())
}
