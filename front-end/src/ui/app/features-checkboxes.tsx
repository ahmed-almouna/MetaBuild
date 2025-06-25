import React from 'react';
import styles from "@/ui/page.module.css";

export default function FeaturesCheckboxes() {
    return (
        <>
            <h6 className='mt-4'>Special Features (beta)</h6>
            <div className="row mx-0 gap-4"> 

                <label htmlFor="feature_silent" className={`card col ${styles.purposeRadioCard}`}>
                    <div className="card-body row align-items-center">
                        <div className="form-check col-auto">
                            <input className="form-check-input" type="checkbox" name="Features" value="Silent" id="feature_silent" style={{cursor: 'pointer'}}/>
                        </div>
                
                        <div className="col-auto">
                            <h6 className="mb-1">Silent</h6>
                            <p className="mb-0 text-muted">Low-noise cooling solution</p>
                        </div>  
                    </div>
                </label>
                
                <label htmlFor="feature_compact" className={`card col  ${styles.purposeRadioCard}`}>
                    <div className="card-body row align-items-center">
                        <div className="form-check col-auto">
                            <input className="form-check-input" type="checkbox" name="Features" value="Compact" id="feature_compact" style={{cursor: 'pointer'}}/>
                        </div>
                
                        <div className="col-auto">
                            <h6 className="mb-1">Compact</h6>
                            <p className="mb-0 text-muted">Small form-factor components</p>
                        </div>  
                    </div>
                </label>

                <label htmlFor="feature_futureproof" className={`card col ${styles.purposeRadioCard}`}>
                    <div className="card-body row align-items-center">
                        <div className="form-check col-auto">
                            <input className="form-check-input" type="checkbox" name="Features" value="Futureproof" id="feature_futureproof" style={{cursor: 'pointer'}}/>
                        </div>
                
                        <div className="col-auto">
                            <h6 className="mb-1">Future-Proof</h6>
                            <p className="mb-0 text-muted">Future-proof components</p>
                        </div>  
                    </div>
                </label>

                <label htmlFor="feature_upgradable" className={`card col ${styles.purposeRadioCard}`}>
                    <div className="card-body row align-items-center">
                        <div className="form-check col-auto">
                            <input className="form-check-input" type="checkbox" name="Features" value="Upgradable" id="feature_upgradable" style={{cursor: 'pointer'}}/>
                        </div>
                
                        <div className="col-auto">
                            <h6 className="mb-1">Upgradable</h6>
                            <p className="mb-0 text-muted">Upgradable components build</p>
                        </div>  
                    </div>
                </label>

            </div>
        </>
    );
}