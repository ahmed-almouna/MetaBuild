'use client';
import { useState } from 'react';
import {formatCurrency} from '@/common/utlis'

export default function Slider() {
    
    const [budget, setBudget] = useState(1600);
    function handleChange(event: React.ChangeEvent<HTMLInputElement>) {
        setBudget(Number(event.target.value));
    }

    return (
    <>
        <label htmlFor="budgetSlider" style={{cursor: 'text'}}><h6>Budget: {formatCurrency.format(budget)}</h6></label>
        <input type='range' className='form-range'
            min='500' 
            max='3000' 
            step='50'
            id='budgetSlider' 
            onChange={handleChange}
            value={budget}
            name='Budget'
        />
        <span className='d-flex justify-content-between'>
            <span className='text-muted'>{formatCurrency.format(500)}</span>
            <span className='text-muted'>{formatCurrency.format(3000)}</span>
        </span>
    </>
    );
}